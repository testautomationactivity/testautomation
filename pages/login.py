import os
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:

    USERNAME = "testautomationactivity"
    PASSWORD = "testautomation2024"
    ERROR_MESSAGE = "Incorrect username or password."

    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, 'login_field')
        self.password_input = (By.ID, 'password')
        self.login_button = (By.NAME, 'commit')
        self.error_message = (By.CLASS_NAME, 'flash-error')
        self.logger = logging.getLogger(__name__)

    def enter_username(self, username):

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.username_input)
            ).send_keys(username)
            self.logger.debug(f"Entered username: {username}")
        except TimeoutException:
            self.logger.error("Username input not found")
            raise

    def enter_password(self, password):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.password_input)
            ).send_keys(password)
            self.logger.debug(f"Entered password: {password}")
        except TimeoutException:
            self.logger.error("Password input not found")
            raise

    def click_login(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.login_button)
            ).click()
            self.logger.debug("Clicked login button")
        except TimeoutException:
            self.logger.error("Login button not clickable")
            raise

    def get_error_message(self):
        try:
            # wait the ready state to be complete
            WebDriverWait(driver=self.driver, timeout=20).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )
            error_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.error_message)
            )
            error_message = error_message_element.text

            # error_message = self.driver.find_element("css selector", ".flash-error").text
            self.logger.debug(f"Error message found: {error_message}")
            self.take_screenshot("failures")
            return error_message
        except TimeoutException:
            self.logger.error("Error message not found")
            return ""

    def take_screenshot(self, file_name):
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.driver.save_screenshot(f'screenshots/{file_name}-{timestamp}.png')
        self.logger.debug(f"Screenshot saved as {file_name}-{timestamp}.png")
