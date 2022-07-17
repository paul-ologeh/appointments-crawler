import time
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


BASE_URL = "https://ais.usvisa-info.com/en-gb/niv"
SIGN_IN_URL = f"{BASE_URL}/users/sign_in"
SIGN_OUT_URL = f"{BASE_URL}/users/sign_out"
SCHEDULE_API = f"{BASE_URL}/schedule/41649206/appointment/days/17.json?appointments[expedite]=false"
RESCHEDULE_APPOINTMENT_URL = f"{BASE_URL}/schedule/41649206/appointment"

driver = webdriver.Chrome()

PAYLOAD = {
    "inUserName": "xxxxxxxxxxx@gmail.com",
    "inUserPass": "xxxxxxxxxxxxxxxxxxxxxx",
}


def sign_in():
    driver.get(SIGN_IN_URL)

    confirm = driver.find_element(By.XPATH, "//input[@id='policy_confirmed']/./..")
    confirm.location_once_scrolled_into_view
    confirm.click()

    username = driver.find_element(By.ID, "user_email")
    username.send_keys(PAYLOAD["inUserName"])

    passsword = driver.find_element(By.ID, "user_password")
    passsword.send_keys(PAYLOAD["inUserPass"])
    passsword.send_keys(Keys.RETURN)

    time.sleep(5)


def is_appointment_available(target_date: datetime = "2022-09-23") -> bool:
    driver.get(SCHEDULE_API)

    html = driver.page_source
    parsed_html = BeautifulSoup(html, features="html.parser")
    appointments = json.loads(parsed_html.body.text)

    if len(appointments) == 0:
        return False

    earliest = datetime.fromisoformat(appointments[0]["date"])
    target = datetime.fromisoformat(target_date)
    if earliest <= target:
        print(earliest)
        return True

    return False


def book_appointment():
    driver.get(RESCHEDULE_APPOINTMENT_URL)

    appointments_date = driver.find_element(
        By.ID, "appointments_consulate_appointment_date_input"
    )
    appointments_date.click()
    # time.sleep(5)

    # date_picker = driver.find_element(By.ID, "ui-datepicker-div")
    # next_date = driver.find_element(By.CLASS_NAME, "ui-state-default")
    # time.sleep(5)
    # while next_date is None:
    #     date_picker.find_element(
    #         By.CLASS_NAME, "ui-datepicker-next ui-corner-all"
    #     ).click()
    #     next_date = date_picker.find_element(By.CLASS_NAME, "ui-state-default")

    # next_date.click()

    return False


def clean_up():
    time.sleep(5)
    driver.get(SIGN_OUT_URL)

    driver.close()


if __name__ == "__main__":
    try:
        sign_in()
        while not is_appointment_available():
            time.sleep(300)

        driver.get(RESCHEDULE_APPOINTMENT_URL)
        while True:
            os.system('say "found a USA VISA embassy appointment"')
            time.sleep(3)
    except KeyboardInterrupt:
        clean_up()
    except Exception as e:
        print(e)
        clean_up()
