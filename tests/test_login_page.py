import pytest
import logging
from pages.login import LoginPage
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("logs/test.log")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def test_invalid_login_wrong_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password("TLpm(mN2Jg;HQxj")
    page_login.click_login()
    errors = page_login.get_error_message()

    assert LoginPage.ERROR_MESSAGE in errors
    logger.info("Invalid login test passed")


def test_invalid_login_wrong_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username("frameworkauto")
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    errors = page_login.get_error_message()

    assert LoginPage.ERROR_MESSAGE in errors
    logger.info("Invalid login test passed")


def test_sql_injection_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username("' OR 1=1 --")
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    error_message = page_login.get_error_message()
    assert LoginPage.ERROR_MESSAGE in error_message
    logger.info("SQL injection test passed")


def test_cross_site_scripting_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username("<script>alert('xss')</script>")
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    error_message = page_login.get_error_message()
    assert LoginPage.ERROR_MESSAGE in error_message
    logger.info("Cross-site scripting test passed")


def test_username_max_length(setup):
    long_username = "a" * 256  # Assuming the max length is 255 characters
    page_login = LoginPage(setup)
    page_login.enter_username(long_username)
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    error_message = page_login.get_error_message()
    assert LoginPage.ERROR_MESSAGE in error_message
    logger.info("Maximum length username test passed")


def test_password_max_length(setup):
    long_password = "a" * 256  # Assuming the max length is 255 characters
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password(long_password)
    page_login.click_login()
    error_message = page_login.get_error_message()
    assert LoginPage.ERROR_MESSAGE in error_message
    logger.info("Maximum length password test passed")


def test_valid_login_username_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()

    try:
        assert "testautomationactivity" in setup.page_source
        logger.info("Valid login test passed")
    except TimeoutException:
        logger.error("Valid login test failed - username not found in page source")
        pytest.fail("Login failed, username title not found in page")
