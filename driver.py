import os

from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver


def create_driver():
    options = ChromeOptions()
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": str(os.getcwd()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
    }
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"

    options.add_experimental_option("prefs", prefs)
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-http2")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("log-level=3")
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent})
    driver.execute_cdp_cmd(
        "Network.setExtraHTTPHeaders",
        {
            "headers": {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "no-cache",
                "dnt": "1",
                "origin": "https://tgeapcet.nic.in",
                "referer": "https://tgeapcet.nic.in/",
                "upgrade-insecure-requests": "1",
            }
        },
    )
    driver.get("https://tgeapcet.nic.in")

    wait = WebDriverWait(driver, 30)

    college_allotment_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "College-wise Allotment Details")))
    college_allotment_link.click()

    original_window = driver.current_window_handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    return driver, wait


def mismatch(driver):
    if "Branch/ College Mismatch " in driver.page_source:
        print("Branch/ College Mismatch detected. Recreating driver and skipping this branch.")
        driver.quit()
        return True
    return False
