from src.video import Video
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values, load_dotenv
from time import sleep
import pickle


class Publisher:
    load_dotenv()
    username = os.getenv("PUBLER_ID")
    password = os.getenv("PUBLER_PASSWORD")

    def __init__(self, video: Video) -> None:
        self.video = video

    def __init_driver(self):
        print("Driver initialized...")
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--log-level=3")
        options.add_argument("--lang=en")
        options.add_experimental_option(
            "excludeSwitches", ["enable-logging", "enable-automation"]
        )
        # options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1280,800")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(
            options=options,
            executable_path="/usr/local/bin/chromedriver-linux64/chromedriver",
        )

    def publish(self):
        self.__init_driver()
        self.__login()
        self.__close_boxes()
        self.__upload_video()
        self.__customize_tik_tok()
        self.__publish_video()
        self.video.status = "done"
        return self.video

    def __next_video_path(self) -> str:
        if self.video.queue_source is None:
            raise Exception("Queue source is not set")
        try:
            queue_source = self.video.queue_source
            part_source = self.video.video_parts[0]
            return queue_source + part_source
        except Exception as e:
            print(e)
            return ""

    def __get_video_title(self) -> str:
        if self.video.title is not None:
            if len(self.video.video_parts) > 1:
                last_bit = self.video.video_parts[0].split("_")[3]
                title_number = int(last_bit.split(".")[0]) + 1
                return f"{self.video.title} - ({title_number}/{len(self.video.video_parts)})"
            # return first 100 characters of title
            return self.video.title[:100]
        return ""

    def __login(self):
        if self.driver is None:
            return 0
        try:
            # load cookies
            self.driver.get("https://app.publer.io/users/sign_in")
            sleep(5)
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.implicitly_wait(1)
            self.driver.get("https://app.publer.io/#")

            sleep(5)
            # Manual login refresh cookie
            current_url = self.driver.current_url
            if current_url == "https://app.publer.io/users/sign_in":
                cookieButton = self.driver.find_element(
                    By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/a"
                )
                self.driver.execute_script("arguments[0].click();", cookieButton)
                self.driver.implicitly_wait(1)
                user_input = self.driver.find_element(
                    By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/form/input[3]"
                )
                self.driver.implicitly_wait(1)
                self.driver.execute_script("arguments[0].click();", user_input)
                user_input.send_keys(self.username)
                self.driver.implicitly_wait(1)
                user_password = self.driver.find_element(
                    By.XPATH,
                    "/html/body/div/div[2]/div[1]/div[2]/form/div[1]/div/input",
                )
                self.driver.execute_script("arguments[0].click();", user_password)
                user_password.send_keys(self.password)
                self.driver.implicitly_wait(1)
                login_button = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="application-container"]/div[2]/div[1]/div[2]/form/input[4]',
                )
                self.driver.execute_script("arguments[0].click();", login_button)
            sleep(30)
            pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

        except Exception as e:
            print(e)
            self.driver.quit()
            exit(1)

    #
    #

    def __close_boxes(self):
        sleep(15)
        x_button = self.driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div/div[2]/button"
        )
        self.driver.execute_script("arguments[0].click();", x_button)

        second_x_button = self.driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div/button"
        )
        sleep(2)
        self.driver.execute_script("arguments[0].click();", second_x_button)

    def __upload_video(self):
        if self.driver is None:
            return 0
        upload_video_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div/div/div/div/div/div[2]/div/span/div/div/div/div/div/div/div/div/div/input",
        )
        sleep(1)
        print("uploading video...:" + self.__next_video_path())
        upload_video_button.send_keys(os.path.abspath(self.__next_video_path()))

        self.driver.implicitly_wait(5)
        customize_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/footer/div[1]/div/div/span[1]/span/span/i",
        )

        self.driver.execute_script("arguments[0].click();", customize_button)
        print("video upload successful")

    def __customize_tik_tok(self):
        sleep(90)
        reminder = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div/div/div/div/div/div[2]/div/span/div/div[2]/div/div/div[2]/div[2]",
        )
        reminder.click()

    def __publish_video(self):
        sleep(60)
        publish_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/footer/div[2]/button[2]",
        )
        self.driver.execute_script("arguments[0].click();", publish_button)

        self.driver.quit()
        print("video publish successful")
