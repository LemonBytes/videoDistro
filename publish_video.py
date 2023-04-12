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
from edit_video import write_to_queue
from time import sleep


def get_first_video_with_parts():
    with open("video_parts.json", "r") as file:
        data = json.load(file)
        videos = data["video_parts"]
        for video in videos:
            if len(video["parts"]) > 0:
                return video
    return {}


def remove_from_queue():
    with open("queue.json", "r") as f:
        data = json.load(f)
        queue = data["queue"]
        if len(queue) > 0:
            cmd = f"rm ./video_upload_queue/{queue[0]['video_src']}"
            subprocess.run(cmd, shell=True)
            queue.pop(0)
    with open("queue.json", "w") as f:
        json.dump(data, f, indent=4)


def clean_up():
    with open("video_parts.json", "r") as f:
        data = json.load(f)
        videos = data["video_parts"]
        for video in videos:
            if len(video["parts"]) > 0:
                video["parts"].pop(0)
    with open("video_parts.json", "w") as f:
        json.dump(data, f, indent=4)


def decide_video_upload():
    if random.random() < 0.3:
        video = get_first_video_with_parts()
        video_id = video["video_id"]
        video_src = video["parts"][0]
        video_part_number = int(video_src.split("_")[-1].split(".")[0]) + 1
        title = video["video_title"] + f"- part {video_part_number}"
        write_to_queue(f"video_parts/{video_id}/{video_src}", video_src, title)
        clean_up()


decide_video_upload()


def get_first_from_queue():
    with open("queue.json", "r") as f:
        data = json.load(f)
        queue = data["queue"]
        if len(queue) > 0:
            video = queue[0]
            return video
    return {}


def login(username, password):
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
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome(
        options=options,
        executable_path="./chromedriver",
    )
    try:
        logged_in = False
        driver.get("https://app.publer.io/users/sign_in")
        sleep(1)
        cookieButton = driver.find_element(
            By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/a"
        )
        driver.execute_script("arguments[0].click();", cookieButton)
        sleep(1)
        user_input = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/form/input[3]"
        )
        sleep(1)
        driver.execute_script("arguments[0].click();", user_input)
        user_input.send_keys(username)
        sleep(1)
        user_password = driver.find_element(
            By.XPATH, "/html/body/div/div[2]/div[1]/div[2]/form/div[1]/div/input"
        )
        driver.execute_script("arguments[0].click();", user_password)
        user_password.send_keys(password)
        sleep(2)
        login_button = driver.find_element(
            By.XPATH,
            '//*[@id="application-container"]/div[2]/div[1]/div[2]/form/input[4]',
        )
        driver.execute_script("arguments[0].click();", login_button)

        print("login successful")
        setup(driver)
    except Exception as e:
        print(e)
        driver.quit()
        exit(1)


def setup(driver):
    banner_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/button")
    sleep(1)
    driver.execute_script("arguments[0].click();", banner_button)
    sleep(1)
    account_number = 1
    while account_number <= 3:
        sleep(1)
        account_button = driver.find_element(
            By.XPATH,
            f"/html/body/div/div[2]/div/main/div/main/div[1]/div[2]/div[{account_number}]/div",
        )
        sleep(1)
        driver.execute_script("arguments[0].click();", account_button)
        sleep(1)
        account_number += 1
    print("setup successful")
    sleep(2)
    upload_video(driver)


def upload_video(driver):
    upload_video_button = driver.find_element(
        By.XPATH,
        "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div/div[2]/div/div/div/div[2]/div/span/div/div/div/div/div/div/div/div/input",
    )
    sleep(1)
    video = get_first_from_queue()
    video_src = video["video_src"]
    title = video["video_title"]
    upload_video_button.send_keys(os.path.abspath(f"./video_upload_queue/{video_src}"))
    sleep(5)
    print("video upload successful")
    customize_video(driver, title)


def customize_video(driver, title):
    customize_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/footer/div[1]/div/div/span[1]/span/span/i",
    )
    driver.execute_script("arguments[0].click();", customize_button)
    sleep(3)
    ########## INSTAGRAM ##########
    fake_label = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div",
    )
    driver.execute_script("arguments[0].click();", fake_label)
    sleep(1)
    reel_button = driver.find_element(
        By.XPATH,
        "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div[1]/div[3]",
    )
    driver.execute_script("arguments[0].click();", reel_button)
    sleep(1)
    aria_label = driver.find_element(
        By.XPATH,
        "/html/body/div/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/div[1]/div/div/div",
    )
    driver.execute_script("arguments[0].click();", aria_label)
    sleep(2)
    ActionChains(driver).send_keys("", title).perform()
    sleep(2)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    for i in range(3):
        ActionChains(driver).send_keys(Keys.ENTER).perform()
        ActionChains(driver).send_keys("", "follow @warofmind_").perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    sleep(1)
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    ActionChains(driver).send_keys(
        "#mma#fighter#boxing#fyp#foryou#trending#ufc#body#sport#martialarts"
    ).perform()

    sleep(2)

    ########## YOUTUBE ##########

    ActionChains(driver).send_keys(Keys.TAB * 2).perform()
    sleep(2)

    ActionChains(driver).send_keys("", title).perform()
    sleep(1)
    ActionChains(driver).send_keys(Keys.TAB * 1).perform()
    ActionChains(driver).send_keys(
        "#mma #fighter #boxing #fyp #foryou #trending #mindbody #body #ufc #martialarts"
    ).perform()
    sleep(1)
    short_button = driver.find_element(
        By.XPATH,
        " /html/body/div[1]/div[2]/div/main/div/main/div[2]/div/div/div[3]/div/div/span/div/div/div[2]/div[3]/div/div/div[1]/div[2]",
    )
    driver.execute_script("arguments[0].click();", short_button)

    sleep(2)
    publish_button = driver.find_element(
        By.XPATH,
        "/html/body/div[1]/div[2]/div/main/div/main/div[2]/footer/div[2]/button[2]",
    )
    driver.execute_script("arguments[0].click();", publish_button)
    sleep(20)
    print("video publish  successful")
    remove_from_queue()
    driver.quit()


def publish_video():
    config = dotenv_values(".env")
    login(config["PUBLER_ID"], config["PUBLER_PASSWORD"])
