#!/usr/bin/env python3
import argparse
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def register_for_asvz_lesson(lesson_id, frequency, attempts) -> None:
    """
    Register for an ASVZ lesson.
    :param attempts: The number of attempts to registration when the lesson has been released.
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
    login_button = driver.find_element(By.XPATH, "/html/body/app-root/div/div["
                                                 "2]/app-lesson-details/div/div/app-lessons-enrollment-button/button")
    login_button.click()
    driver.implicitly_wait(5)
    login_user_name = driver.find_element(By.ID, "AsvzId")
    # Todo: Add you username here.
    login_user_name.send_keys("your_username")

    login_password = driver.find_element(By.ID, "Password")
    # Todo: Add you password here.
    login_password.send_keys("your_password")
    # Find the submit button.
    submit = driver.find_element(By.XPATH, '/html/body/div/div[5]/div[1]/div/div[2]/div/form/div[3]/button')
    submit.click()
    driver.implicitly_wait(5)
    # After logging in, if the register button cannot be found, the lesson is fully booked.
    if len(driver.find_elements(By.ID, "btnRegister")) == 0:
        print("The lesson has been fully booked!")
        return

    # https://stackoverflow.com/questions/44759907/find-element-by-class-name-for-multiple-classes
    print_once_flag = True
    try:
        # Check whether the button is clickable or not.
        while len(driver.find_elements(By.CSS_SELECTOR, ".disabled")) != 0:
            # If the button is not clickable, refresh it at a certain frequency.
            driver.refresh()
            driver.implicitly_wait(1 / frequency)
            if print_once_flag:
                print(f"The lesson registration is not open, refreshing at {frequency}Hz.")
                print_once_flag = False
    except KeyboardInterrupt as e:
        print(e)
        return
    # Once the button is clickable, it would not be disabled.
    while attempts > 0:
        try:
            register_button = driver.find_element(By.ID, "btnRegister")
            register_button.click()
            print("The lesson has been registered successfully!")
            return
        except (StaleElementReferenceException, NoSuchElementException) as e:
            attempts = attempts - 1
            print(f"Remaining attempt times: {attempts}...")

    print("The lesson registration failed.")


def main():
    my_parser = argparse.ArgumentParser(
        description="ASVZ lesson registration.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    my_parser.add_argument(
        '-i', '--id', help='The ASVZ lesson ID.', type=str, required=True)
    my_parser.add_argument(
        '-f', '--frequency', help='The refreshing frequency for registration. The frequency should be <= 0.5Hz to '
                                  'allow page loading during refreshing', default=0.5)
    my_parser.add_argument(
        '-attempts', '--attempts', help='The number of attempts to register when the lesson has been released.',
        default=50)
    my_args = my_parser.parse_args()
    register_for_asvz_lesson(my_args.id, my_args.frequency, my_args.attempts)


if __name__ == '__main__':
    main()
