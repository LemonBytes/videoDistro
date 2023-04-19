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


    def __init__(self, video:Video) -> None:
        self.video = video

    def __init_driver(self):
        if self.driver is None:
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
            self.__init_driver()
        else:
            return 0

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
            
           