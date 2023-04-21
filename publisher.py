from video import Video
import json
import os
import random
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import dotenv_values
from time import sleep


class Publisher:
    driver = None
    config = dotenv_values(".env")
    username = config["PUBLER_ID"]
    password = config["PUBLER_PASSWORD"]
    video_title = None

    def __init__(self, video: Video, next_upload_number: int) -> None:
        self.video = video
        self.next_upload_number = next_upload_number
        self.__init_driver()

    def __init_driver(self):
        if self.driver is not None:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--log-level=3")
            options.add_argument("--lang=en")
            options.add_experimental_option(
                "excludeSwitches", ["enable-logging", "enable-automation"]
            )
            options.add_argument("window-size=1280,800")
            # options.add_argument("--headless")
            # options.add_argument("--disable-gpu")
            # self.driver = webself.driver.Chrome(options=options)
            self.driver = self.driver.Chrome(
                options=options,
                executable_path="./chromeself.driver",
            )

    def __next_video_path_from_queue(self) -> str:
        # get the first folder in the video_upload_queue
        video_path = os.listdir("./video_upload_queue")[0]
        # get the first video in the folder
        video_path = os.listdir(f"./video_upload_queue/{video_path}")[0]
        return video_path

    def __get_video_title(self, video_id):
        with open("videos.json", "r") as f:
            data = json.load(f)
            videos = data["video_parts"]
            for video in videos:
                if video["video_id"] == self.video.id:
                    return video["video_title"]

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
            banner_button = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/button"
            )
            sleep(1)
            self.driver.execute_script("arguments[0].click();", banner_button)
            sleep(1)
            account_number = 1
            while account_number <= 3:
                sleep(1)
                account_button = self.driver.find_element(
                    By.XPATH,
                    f"/html/body/div/div[2]/div/main/div/main/div[1]/div[2]/div[{account_number}]/div",
                )
                sleep(1)
                self.driver.execute_script("arguments[0].click();", account_button)
                sleep(1)
                account_number += 1
            print("setup successful")
            sleep(2)

        def __upload_video(self):
            upload_video_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/span/div/div/div/div/div/div/div/div/input",
            )
            sleep(1)
            if self.upload_type == "queue":
                video_src = self.__video_path()
                video_id = video_src.split("_")[0]
                self.video_title = self.__get_video_title(video_id)
            else:
                video_src = f"./video_upload_queue/{self.next_upload_number}_{self.video.id}/{self.video.id}_video.mp4"
                self.video_title = self.video.title

            upload_video_button.send_keys(
                os.path.abspath(f"./video_upload_queue/{video_src}")
            )
            self.driver.implicitly_wait(5)
            print("video upload successful")

        def __customize_instgram_upload(self):
            customize_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/footer/div[1]/div/div/span[1]/span/span/i",
            )
            self.driver.execute_script("arguments[0].click();", customize_button)
            sleep(3)
            ########## INSTAGRAM ##########
            fake_label = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div",
            )
            self.driver.execute_script("arguments[0].click();", fake_label)
            sleep(1)
            reel_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div[1]/div[3]",
            )
            self.driver.execute_script("arguments[0].click();", reel_button)
            sleep(1)
            aria_label = self.driver.find_element(
                By.XPATH,
                "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div",
            )
            self.driver.execute_script("arguments[0].click();", aria_label)
            sleep(2)
            ActionChains(self.driver).send_keys("", self.video_title).perform()
            sleep(2)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            for i in range(3):
                ActionChains(self.driver).send_keys(Keys.ENTER).perform()
                ActionChains(self.driver).send_keys("", "follow @warofmind_").perform()
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            ActionChains(self.driver).send_keys(
                "#mma#fighter#boxing#fyp#foryou#trending#ufc#body#sport#martialarts"
            ).perform()
            sleep(2)

        def __customize_youtube_upload(self):
            ActionChains(self.driver).send_keys(Keys.TAB * 2).perform()
            sleep(2)

            ActionChains(self.driver).send_keys("", self.video_title).perform()
            sleep(1)
            ActionChains(self.driver).send_keys(Keys.TAB * 1).perform()
            ActionChains(self.driver).send_keys(
                "#mma #fighter #boxing #fyp #foryou #trending #mindbody #body #ufc #martialarts"
            ).perform()
            sleep(1)
            short_button = self.driver.find_element(
                By.XPATH,
                " /html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[3]/div/div/div[1]/div[2]",
            )
            self.driver.execute_script("arguments[0].click();", short_button)

            sleep(2)
            publish_button = self.driver.find_element(
                By.XPATH,
                "/html/body/div[1]/div[2]/div/main/div/main/div[2]/footer/div[2]/button[2]",
            )
            self.driver.execute_script("arguments[0].click();", publish_button)
            sleep(20)
            self.driver.quit()

            def publish(self, upload_type: str):
                self.__login()
                self.__setup()
                self.__upload_video(upload_type)
                self.__customize_instgram_upload()
                self.__customize_youtube_upload()
