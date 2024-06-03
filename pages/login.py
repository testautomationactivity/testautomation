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
    VALIDATION_MESSAGE = "Please fill in this field."

    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "login_field")
        self.username_label = (By.XPATH, '//label[@for="login_field"]')
        self.password_label = (By.XPATH, '//label[@for="password"]')
        self.header_label = (By.XPATH, '//*[@id="login"]/div[1]/h1')
        self.password_input = (By.ID, "password")
        self.forgot_password_link = (By.LINK_TEXT, "Forgot password?")
        self.create_account_link = (By.LINK_TEXT, "Create an account")
        self.sign_in_with_passkey_option = (By.ID, "sign_in_with_passkey")
        self.login_button = (By.NAME, "commit")
        self.error_message = (By.CLASS_NAME, "flash-error")
        self.footer_labels = [
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[1]'),
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[2]'),
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[3]'),
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[4]'),
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[5]'),
            (By.XPATH, '//ul[contains(@class, "list-style-none")]/li[6]'),
        ]
        self.logger = logging.getLogger(__name__)

    def enter_username(self, username):

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.username_input)
            ).send_keys(username)
            self.logger.debug(f"Entered username: {username}")
        except TimeoutException:
            self.logger.error("Username input not found")
            raise

    def enter_password(self, password):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.password_input)
            ).send_keys(password)
            self.logger.debug(f"Entered password: {password}")
        except TimeoutException:
            self.logger.error("Password input not found")
            raise

    def click_login(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.login_button)
            ).click()
            self.logger.debug("Clicked login button")
            self.take_screenshot("submit")
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
            self.take_screenshot("PageError")
            # error_message = self.driver.find_element("css selector", ".flash-error").text
            self.logger.debug(f"Error message found: {error_message}")

            return error_message
        except TimeoutException:
            self.logger.error("Error message not found")
            self.take_screenshot("failures")
            return ""

    def get_validation_message(self):
        username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        assert (
            username.get_attribute("validationMessage") == "Please fill out this field."
        )

    def get_username_label(self):
        try:
            label = (
                WebDriverWait(self.driver, 10)
                .until(EC.visibility_of_element_located(self.username_label))
                .text
            )
            self.logger.info(f"Username label found: {label}")
            return label
        except TimeoutException:
            self.logger.error("Username label not found")
            self.take_screenshot("username_label_not_found")
            return ""

    def get_password_label(self):
        try:
            label = (
                WebDriverWait(self.driver, 10)
                .until(EC.visibility_of_element_located(self.password_label))
                .text
            )
            self.logger.info(f"Password label found: {label}")
            return label
        except TimeoutException:
            self.logger.error("Password label not found")
            self.take_screenshot("password_label_not_found")
            return ""

    def get_header_label(self):
        try:
            label = (
                WebDriverWait(self.driver, 10)
                .until(EC.visibility_of_element_located(self.header_label))
                .text
            )
            self.logger.info(f"Header label found: {label}")
            return label
        except TimeoutException:
            self.logger.error("Header label not found")
            self.take_screenshot("header_label_not_found")
            return ""

    def click_forgot_password(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.forgot_password_link)
            ).click()
            self.logger.info("Clicked 'Forgot password?' link")
        except TimeoutException:
            self.logger.error("'Forgot password?' link not responding")
            raise

    def click_create_account(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.create_account_link)
            ).click()
            WebDriverWait(self.driver, 10).until(EC.title_contains("Join GitHub"))
            self.logger.info("Clicked 'Create an account' link")
        except TimeoutException:
            self.logger.error("'Create an account' link not responding")
            raise

    def get_footer_labels(self):
        try:
            labels = []
            for footer_label in self.footer_labels:
                label_text = (
                    WebDriverWait(self.driver, 10)
                    .until(EC.visibility_of_element_located(footer_label))
                    .text
                )
                labels.append(label_text)
            self.logger.info(f"Page footer labels found: {labels}")
            return labels
        except TimeoutException:
            self.logger.error("Login page Footer labels NOT found")
            self.take_screenshot("footer_labels_not_found")
            return []

    def is_sign_in_with_passkey_option_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.sign_in_with_passkey_option)
            )
            self.logger.info("Sign in with passkey option found")
            return True
        except TimeoutException:
            self.logger.error("Sign in with passkey option not found")
            return False

    def take_screenshot(self, file_name):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.driver.save_screenshot(f"screenshots/{file_name}-{timestamp}")
        self.logger.debug(f"Screenshot saved as {file_name}-{timestamp}.png")
