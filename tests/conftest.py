import pytest
from selenium import webdriver


@pytest.fixture(scope="module")
def setup(request):
    # Initialize the WebDriver (Chrome) instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run in headless mode for Docker
    chrome_options.add_argument("--use_subprocess")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://github.com/login")

    driver.maximize_window()

    # Yield the driver instance to the tests
    yield driver

    # Quit the driver after tests are done
    driver.delete_all_cookies()
    driver.quit()


def pytest_html_report_title(report):
    report.title = "Login Automation Test Report"