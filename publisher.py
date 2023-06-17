from video import Video
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
from dotenv import dotenv_values
from time import sleep


class Publisher:
    config = dotenv_values(".env")
    username = config["PUBLER_ID"]
    password = config["PUBLER_PASSWORD"]

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
        options.add_argument("window-size=1280,800")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(
            options=options,
            executable_path="./chromedriver",
        )

    def publish(self):
        self.__init_driver()
        self.__login()
        self.__setup()
        self.__upload_video()
        self.__customize_youtube_upload()
        self.__customize_instgram_upload()
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
                return f"{self.video.title} - Part {title_number}"
            # return first 100 characters of title
            return self.video.title[:100]
        return ""

    def __login(self):
        if self.driver is None:
            return 0
        try:
            self.driver.get("https://app.publer.io/users/sign_in")
            self.driver.implicitly_wait(1)
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
                By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/form/div[1]/div/input"
            )
            self.driver.execute_script("arguments[0].click();", user_password)
            user_password.send_keys(self.password)
            self.driver.implicitly_wait(1)
            login_button = self.driver.find_element(
                By.XPATH,
                '//*[@id="application-container"]/div[2]/div[1]/div[2]/form/input[4]',
            )
            self.driver.execute_script("arguments[0].click();", login_button)
        except Exception as e:
            print(e)
            self.driver.quit()
            exit(1)

    def __setup(self):
        if self.driver is None:
            return 0

        self.driver.implicitly_wait(10)
        banner_button = self.driver.find_element(
            By.XPATH, "/html/body/div[3]/div/div/button"
        )
        sleep(1)
        self.driver.execute_script("arguments[0].click();", banner_button)
        sleep(1)
        account_number = 3
        while account_number >= 1:
            sleep(1)
            account_button = self.driver.find_element(
                By.XPATH,
                f"/html/body/div/div[2]/div/main/div/main/div[1]/div[2]/div[{account_number}]/div",
            )
            self.driver.execute_script("arguments[0].click();", account_button)
            sleep(1)
            account_number -= 1
        print("setup successful")
        sleep(2)

    def __upload_video(self):
        if self.driver is None:
            return 0
        upload_video_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/span/div/div/div/div/div/div/div/div/div/input",
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

    def __customize_youtube_upload(self):
        if self.driver is None:
            return 0

        youtubeInput = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div[1]",
        )
        youtubeInput.click()
        ActionChains(self.driver).send_keys("", self.__get_video_title()).perform()

        ActionChains(self.driver).send_keys(Keys.TAB * 1).perform()

        ActionChains(self.driver).send_keys(
            "Welcome, young warriors! Fighting  is not just an adrenaline-packed display of skilled fighters engaging in combat sports. It's an opportunity to learn from the best and develop a deeper understanding of the techniques."
        ).perform()
        sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        ActionChains(self.driver).send_keys(
            "Fighting inspire and motivate us to push beyond our limits and achieve greatness. It's a way of life. It's a mindset. It's a war of mind."
        ).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        ActionChains(self.driver).send_keys(
            "Join us on our channel to become the ultimate warrior and develop your skills, mindset, and spirit. Hit that subscribe button and let's start the journey together!"
        ).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        ActionChains(self.driver).send_keys(
            "Follow us on Instagram: https://www.instagram.com/warofmind_/"
        ).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        ActionChains(self.driver).send_keys(
            "Follow us on TikTok: https://www.tiktok.com/@__war_of_mind__"
        ).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        ActionChains(self.driver).send_keys(
            "#mma #fighter #boxing #foryou #ufc #martialarts #short #shorts"
        ).perform()
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        sleep(1)
        short_button = self.driver.find_element(
            By.XPATH,
            "//div[contains(text(), 'Short')]",
        )
        self.driver.execute_script("arguments[0].click();", short_button)
        sleep(2)
        ActionChains(self.driver).send_keys(Keys.TAB * 4).perform()

    def __customize_tik_tok(self):
        reminder = self.driver.find_element(
            By.XPATH,
            '//div[@class="u-cursor-pointer u-align-children-center u-width-max-content u-display-inline-flex radio__group__input u-margin-right-10 is-active undefined u-margin-top-10"]',
        )
        self.driver.execute_script("arguments[0].click();", reminder)
        ActionChains(self.driver).send_keys(Keys.TAB * 2).perform()

    def __customize_instgram_upload(self):
        if self.driver is None:
            return 0

        ActionChains(self.driver).send_keys("", self.__get_video_title()).perform()
        sleep(2)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        for i in range(3):
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            ActionChains(self.driver).send_keys("", "follow @warofmind_").perform()
        ActionChains(self.driver).send_keys(Keys.ENTER * 2).perform()
        sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        ActionChains(self.driver).send_keys(
            "#mma#fighter#boxing#fyp#foryou#ufc#body#sport#martialarts"
        ).perform()
        sleep(2)
        reel_button = self.driver.find_element(
            By.XPATH,
            "//div[contains(text(), 'Reel')]",
        )
        self.driver.execute_script("arguments[0].click();", reel_button)

    def __publish_video(self):
        publish_button = self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div/main/div/main/div[2]/footer/div[2]/button[2]",
        )
        self.driver.execute_script("arguments[0].click();", publish_button)
        sleep(15)
        self.driver.quit()
        print("video publish successful")
