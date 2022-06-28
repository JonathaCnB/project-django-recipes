from pathlib import Path

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver.exe"
CHROMEDRIVER_PATH = ROOT_PATH / "chromedriver" / CHROMEDRIVER_NAME
SELENIUM_HEADLESS = settings.SELENIUM_HEADLESS


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if SELENIUM_HEADLESS:
        chrome_options.add_argument("--headless")

    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    # --headless -> Agir sem abrir o navegador
    browser = make_chrome_browser()
    browser.get("http://localhost:8000/")
