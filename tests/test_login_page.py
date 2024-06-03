import pytest
from pages.login import LoginPage
from selenium.common.exceptions import TimeoutException


def test_valid_login_username_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()

    try:
        assert "testautomationactivity" in setup.page_source

    except TimeoutException:
        page_login.take_screenshot("Valid_login_Fail")
        pytest.fail("Login failed")


def test_invalid_login_wrong_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password("TLpm(mN2Jg;HQxj")
    page_login.click_login()
    errors = page_login.get_error_message()

    assert LoginPage.ERROR_MESSAGE in errors


def test_invalid_login_wrong_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username("frameworkauto")
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    errors = page_login.get_error_message()

    assert LoginPage.ERROR_MESSAGE in errors


def test_empty_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    password_input = setup.find_element(*page_login.username_input)
    validation_message = password_input.get_attribute("validationMessage")

    assert validation_message == LoginPage.VALIDATION_MESSAGE


def test_empty_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.click_login()
    password_input = setup.find_element(*page_login.password_input)
    validation_message = password_input.get_attribute("validationMessage")

    assert validation_message == LoginPage.VALIDATION_MESSAGE


def test_empty_username_and_password(setup):
    page_login = LoginPage(setup)
    page_login.click_login()
    password_input = setup.find_element(*page_login.username_input)
    validation_message = password_input.get_attribute("validationMessage")

    assert validation_message == LoginPage.VALIDATION_MESSAGE


def test_username_label_displayed(setup):
    page_login = LoginPage(setup)
    label_text = page_login.get_username_label()
    assert label_text == "Username or email address"


def test_password_label_displayed(setup):
    page_login = LoginPage(setup)
    label_text = page_login.get_password_label()
    assert label_text == "Password"


def test_header_label(setup):
    page_login = LoginPage(setup)
    header_label = page_login.get_header_label()
    assert header_label == "Sign in to GitHub"


def test_forgot_password_link(setup):
    page_login = LoginPage(setup)
    page_login.click_forgot_password()
    assert "Reset your password" in setup.page_source


def test_create_account_link(setup):
    page_login = LoginPage(setup)
    page_login.click_create_account()
    assert "Join GitHub · GitHub" in setup.title


def test_footer_labels(setup):
    page_login = LoginPage(setup)
    expected_labels = [
        "Terms",
        "Privacy",
        "Docs",
        "Contact GitHub Support",
        "Manage cookies",
        "Do not share my personal information",
    ]
    footer_labels = page_login.get_footer_labels()

    assert footer_labels == expected_labels


def test_sign_in_with_passkey_option_present(setup):
    page_login = LoginPage(setup)
    page_login.is_sign_in_with_passkey_option_present()


def test_leading_trailing_spaces_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(f"  {LoginPage.USERNAME}  ")
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()

    try:
        assert "testautomationactivity" in setup.page_source

    except TimeoutException:
        page_login.take_screenshot("Valid_login_Fail")
        pytest.fail("Login failed")


def test_leading_trailing_spaces_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password(f"  {LoginPage.PASSWORD}  ")
    page_login.click_login()

    try:
        assert "testautomationactivity" in setup.page_source

    except TimeoutException:
        page_login.take_screenshot("Valid_login_Fail")
        pytest.fail("Login failed")


def test_case_sensitivity_username(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME.upper())
    page_login.enter_password(LoginPage.PASSWORD)
    page_login.click_login()
    try:
        assert "testautomationactivity" in setup.page_source

    except TimeoutException:
        page_login.take_screenshot("Valid_login_Fail")
        pytest.fail("Login failed")


def test_case_sensitivity_password(setup):
    page_login = LoginPage(setup)
    page_login.enter_username(LoginPage.USERNAME)
    page_login.enter_password(LoginPage.PASSWORD.upper())
    page_login.click_login()
    error_message = page_login.get_error_message()
    assert LoginPage.ERROR_MESSAGE in error_message
