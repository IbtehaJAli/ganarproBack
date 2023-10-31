#!/usr/bin/env python3
# requires: pip install splinter
import argparse
import datetime
import os
import shutil
import time
from urllib.parse import urlparse
from pathlib import Path
import splinter
from selenium import webdriver


def take_screenshot(url, name=None, headless=True, width=None, height=None, wait=None):
    if name is None:
        now = datetime.datetime.now()
        date_time = now.isoformat().split(".")[0]
        name = f"{date_time}-{urlparse(url).netloc}-"
    browser = splinter.Browser("chrome", headless=headless)
    if width is not None and height is not None:
        browser.driver.set_window_size(width, height)
    browser.visit(url)
    if wait is not None:
        time.sleep(wait)
    tmp_filename = Path(Browser.screenshot(name=name, full=True))
    name = tmp_filename.name.rsplit("-", maxsplit=1)[0]
    extension = tmp_filename.name.rsplit(".", maxsplit=1)[-1]
    filename = tmp_filename.parent / (name + "." + extension)
    shutil.move(tmp_filename, filename)
    browser.quit()
    return filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=1280)
    parser.add_argument("--height", default=960)
    parser.add_argument("--no-headless", action="store_true")
    parser.add_argument("--wait", default=3)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--filename")
    parser.add_argument("--filepath")
    parser.add_argument("url")
    args = parser.parse_args()
    filepath, filename = None, None
    if args.filepath:
        filepath = Path(args.filepath)
        if not filepath.exists():
            filepath.mkdir(parents=True)
    if args.filename:
        filename = Path(args.filename)

    screenshot_filename = take_screenshot(
        url=args.url,
        width=args.width,
        height=args.height,
        headless=not args.no_headless,
        wait=args.wait,
    )

    if filepath is not None and filename is not None:
        output_filename = filepath / filename
    elif filepath is not None and filename is None:
        output_filename = filepath / screenshot_filename.name
    elif filepath is None and filename is not None:
        output_filename = filename
    else:  # Move to current working directory
        output_filename = Path(os.getcwd()) / screenshot_filename.name
    shutil.move(screenshot_filename, output_filename)
    if not args.quiet:
        print(output_filename)


if __name__ == "__main__":
    # main()
    def get_screenshot(url='https://www.linkedin.com/company/ganarpro'):
        options = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                     ' Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 960)
        driver.get(url)

        height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(1280, 700)
        # sleep(10)
        driver.save_screenshot(f"test.png")

        driver.quit()


    get_screenshot()

# if __name__ == "__main__":
#     # main()
#     def get_screenshot(url='https://www.linkedin.com/company/ganarpro'):
#         options = webdriver.ChromeOptions()
#         user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' \
#                      ' Chrome/60.0.3112.50 Safari/537.36'
#
#         options.add_argument(f'user-agent={user_agent}')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--headless')
#         options.add_argument('--disable-gpu')
#
#         driver = webdriver.Chrome(options=options)
#         driver.get('https://linkedin.com/')
#         time.sleep(1)
#
#         ### get username and password input boxes path
#         username = driver.find_elements(By.XPATH,'//*[@id="session_key"]')[0]
#         print(username)
#
#         password = driver.find_elements(By.XPATH,'//*[@id="session_password"]')[0]
#
#         ### input the email id and password
#         username.send_keys("r*****a@gmail.com")
#         password.send_keys("Enter_your_password")
#
#         ### click the login button
#         login_btn = driver.find_elements(By.XPATH, "//button[@type='submit']")[0]
#         print(login_btn)
#         time.sleep(1)
#         login_btn.click()
#         driver.set_window_size(1280, 960)
#         driver.get(url)
#
#         height = driver.execute_script("return document.body.scrollHeight")
#         driver.set_window_size(1280, height + 100)
#         # sleep(10)
#         driver.save_screenshot(f"test.png")
#
#         driver.quit()
#
#
#     get_screenshot()