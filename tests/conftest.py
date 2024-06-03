import pytest
import docker
import os
import time
from selenium import webdriver
from base.logger import configure_logging
from webdriver_manager.chrome import ChromeDriverManager
from docker.errors import DockerException, APIError
from tests.errors import DockerSetupException


@pytest.fixture(scope="session")
def docker_container():
    try:
        client = docker.from_env()

        # Build the Docker image
        image_tag = "test-automation-activity:latest"
        client.images.build(path=".", tag=image_tag)

        # Start the Docker container
        container = client.containers.run(
            image_tag,
            detach=True,
            auto_remove=True,
            ports={"4444/tcp": 4444},  # Map the ports if needed
            volumes={
                f"{os.getcwd()}/logs": {"bind": "/app/logs", "mode": "rw"},
                f"{os.getcwd()}/report.html": {
                    "bind": "/app/report.html",
                    "mode": "rw",
                },
            },
        )

        # Allow some time for the container to start
        time.sleep(10)
    except (APIError, DockerException) as e:
        raise DockerSetupException(f"Setup error {e}") from e

    yield container

    # Stop and remove the container after the tests
    container.stop()
    container.remove()


@pytest.fixture(scope="function")
def setup(docker_container):
    # Initialize the WebDriver (Chrome) instance
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")  # Run in headless mode for Docker
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_service = webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get("https://github.com/login")

    driver.maximize_window()

    # Yield the driver instance to the tests
    yield driver

    # Quit the driver after tests are done
    # logger.debug("Browser fixture tear down")
    driver.delete_all_cookies()
    driver.quit()


def pytest_html_report_title(report):
    report.title = "Github Login Page Automation Test Report"


def pytest_configure():
    configure_logging()
