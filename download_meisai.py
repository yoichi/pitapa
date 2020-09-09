#!/usr/bin/env python
import getpass
import time

from invoke import run
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import requests


def wait_port(host, port):
    while True:
        print(f'wait_port({host}, {port})')
        try:
            response = requests.get(f'http://{host}:{port}')
            response.raise_for_status()
            break
        except requests.exceptions.RequestException:
            time.sleep(1.0)

def create(host, port, downloads):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_experimental_option('prefs', {
        'download.default_directory': downloads,
    })

    return webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub',
                            desired_capabilities=options.to_capabilities(),
                            options=options)

def download_meisai(driver, user, password, yyyymm):
    driver.get('https://www.pitapa.com')
    driver.find_element_by_id('h_menu_sub_login').click()
    WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_name('id').send_keys(user)
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('login').click()
    driver.find_element_by_link_text('ご利用代金・明細照会').click()
    meisai_select = driver.find_elements_by_name('claimYM')[-1]
    Select(meisai_select).select_by_value(yyyymm)
    driver.find_element_by_name('displaySubmit').click()
    driver.find_element_by_name('csvSubmit').click()


def wait_download(container, path):
    while True:
        print(f'wait_download({container}, {path})')
        try:
            run(f'docker exec {container} test -e {path}')
            break
        except Exception:
            time.sleep(1.0)


def main(yyyymm):
    host = 'localhost'
    port = 4444
    downloads = '/home/seluser/Downloads'
    user = input('ID: ')
    password = getpass.getpass()
    result = run(f'docker run -d --rm -p {port}:4444 selenium/standalone-chrome')
    container = result.stdout.rstrip()
    try:
        wait_port(host, port)
        driver = create(host, port, downloads)
        download_meisai(driver, user, password, yyyymm)
        csv = f'{downloads}/{yyyymm}.csv'
        wait_download(container, csv)
        run(f'docker cp {container}:{csv} ./')
        driver.quit()
    finally:
        run(f'docker kill {container}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f'usage: {sys.argv[0]} YYYYMM')
        sys.exit(1)
    main(sys.argv[1])
