#!/usr/bin/env python3
import argparse
from enum import Enum
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class LessonState(Enum):
    """
    There are four states for a lesson.
    1. The lesson registration is not open, prior to registration.
    2. The lesson registration is open and it can be registered for.
    3. The lesson registration is open and it has been fully booked.
    4. The lesson registration deadline is passed.
    """
    NOT_OPEN = 1
    OPEN_AVAILABLE = 2
    OPEN_FULLY_BOOKED = 3
    DEADLINE_PASSED = 4
    UNKNOWN = 5


def asvz_account_login(web_driver, username, password):
    """
    Use ASVZ membership account to login
    :param web_driver: selenium.webdriver object.
    :param username: The username of the ASVZ membership account.
    :param password: The password of the ASVZ membership account.
    :return: None
    """
    login_user_name = web_driver.find_element(By.ID, "AsvzId")
    login_password = web_driver.find_element(By.ID, "Password")
    login_user_name.send_keys(username)
    login_password.send_keys(password)
    # Find the submit button.
    submit = web_driver.find_element(By.XPATH, '//button[text()="Login"]')
    submit.click()


def asvz_eth_portal_login(web_driver, username, password):
    """
    Use ETH Zurich university account to login
    :param web_driver: selenium.webdriver object.
    :param username: The username of the ETH Zurich university account.
    :param password: The password of the ETH Zurich university account.
    :return: None
    """
    aai_login_button = web_driver.find_element(By.NAME, "provider")
    aai_login_button.click()
    web_driver.implicitly_wait(5)
    drop_down_button = web_driver.find_element(By.ID, "userIdPSelection_iddicon")
    drop_down_button.click()
    web_driver.implicitly_wait(1)
    aai_portal = web_driver.find_element(By.XPATH, "//div[@title='Universities: ETH Zurich']")
    aai_portal.click()
    web_driver.implicitly_wait(5)

    login_user_name = web_driver.find_element(By.ID, "username")
    login_password = web_driver.find_element(By.ID, "password")
    submit = web_driver.find_element(By.XPATH, '//button[text()="Login"]')
    login_user_name.send_keys(username)
    login_password.send_keys(password)
    submit.click()
    # Todo (GZ): need to verify whether the page is login successfully.


def get_lesson_state(web_driver):
    """
    Get the lesson state.
    :param web_driver: selenium.webdriver object.
    :return: The lesson state.
    """
    lessons_enrollment_alert_button = web_driver.find_elements(By.XPATH, "//*/app-lessons-enrollment-button/alert/div")
    if len(lessons_enrollment_alert_button) != 0:
        if lessons_enrollment_alert_button[0].text == "Die Anmeldefrist ist vorbei.":
            lesson_state = LessonState.DEADLINE_PASSED
            print("Lesson state is: DEADLINE_PASSED")
        elif lessons_enrollment_alert_button[0].text == "Die Lektion ist ausgebucht, du kannst dich daher nicht mehr " \
                                                        "dafür einschreiben.":
            lesson_state = LessonState.OPEN_FULLY_BOOKED
            print("Lesson state is: OPEN_FULLY_BOOKED")
        else:
            lesson_state = LessonState.UNKNOWN
            print("Lesson state is: UNKNOWN")
    else:
        if len(web_driver.find_elements(By.CSS_SELECTOR, ".disabled")) != 0:
            lesson_state = LessonState.NOT_OPEN
            print("Lesson state is: NOT_OPEN")
        else:
            lesson_state = LessonState.OPEN_AVAILABLE
            print("Lesson state is: OPEN_AVAILABLE")
    return lesson_state


def register_for_asvz_lesson(lesson_id, frequency, aai_login) -> None:
    """
    Register for an ASVZ lesson.
    :param aai_login: Enable login by SWITCHaai ETH Zurich.
    :param frequency: The refreshing frequency for registration.
    :param lesson_id: The lesson id, which can be found from the website.
    :return: None
    """
    registration_link = f"https://schalter.asvz.ch/tn/lessons/{lesson_id}"
    # Using Chrome to access web
    s = Service(ChromeDriverManager().install())
    op = webdriver.ChromeOptions()
    # This disables website opening.
    op.add_argument('headless')
    driver = webdriver.Chrome(service=s, options=op)
    driver.get(registration_link)
    driver.implicitly_wait(5)
    # Find the login button.
    login_button = driver.find_element(By.XPATH, "//*/app-lessons-enrollment-button/button")
    login_button.click()
    driver.implicitly_wait(5)
    if not aai_login:
        # Todo: add your ASVZ membership account username and password here.
        asvz_account_login(driver, "your_username", "your_password")
    else:
        # Todo: add your University account username and password here.
        asvz_eth_portal_login(driver, "your_username", "your_password")

    driver.implicitly_wait(5)
    lesson_state = get_lesson_state(driver)

    while True:
        if lesson_state == LessonState.DEADLINE_PASSED:
            print("The lesson registration period is over. Exiting the program...")
            return
        elif lesson_state == LessonState.NOT_OPEN:
            try:
                # Refresh the webpage until the lesson_state changes.
                while lesson_state == LessonState.NOT_OPEN:
                    print(f"The lesson registration is not open, refreshing at {frequency}Hz.")
                    driver.refresh()
                    lesson_state = get_lesson_state(driver)
                    driver.implicitly_wait(1 / frequency)
            except KeyboardInterrupt as e:
                return
        elif lesson_state == LessonState.OPEN_AVAILABLE:
            # Once the button is clickable, proceed to register.
            try:
                register_button = driver.find_element(By.ID, "btnRegister")
                register_button.click()
                driver.implicitly_wait(10)
                print("The lesson has been registered successfully!")
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print("The lesson registration failed. {}. Retrying...".format(e))
                continue
            return
        elif lesson_state == LessonState.OPEN_FULLY_BOOKED:
            try:
                # Refresh the webpage until the lesson_state changes.
                while lesson_state == LessonState.OPEN_FULLY_BOOKED:
                    print(f"The lesson is fully booked, refreshing at {frequency}Hz.")
                    driver.refresh()
                    lesson_state = get_lesson_state(driver)
                    driver.implicitly_wait(1 / frequency)
            except KeyboardInterrupt as e:
                return
        else:
            print("Unknown lesson state. Retrying...")
            continue


def main():
    my_parser = argparse.ArgumentParser(
        description="ASVZ lesson registration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    my_parser.add_argument(
        '-i', '--id', help='The ASVZ lesson ID.', type=str, required=True)
    my_parser.add_argument(
        '-f', '--frequency', help='The refreshing frequency for registration. The frequency should be <= 0.5Hz to '
                                  'allow page loading during refreshing', type=int, default=0.5)
    my_parser.add_argument('--SWITCHaai-ETH', action='store_true', help='Enable login by SWITCHaai ETH Zurich.')
    my_args = my_parser.parse_args()
    register_for_asvz_lesson(my_args.id, my_args.frequency, my_args.SWITCHaai_ETH)


if __name__ == '__main__':
    main()
