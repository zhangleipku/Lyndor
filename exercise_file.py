#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Download exercise file '''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import install, message, read
import os, sys, time, shutil
from colorama import Fore

def download(url, course_folder):
    ''' Download exercise file '''
    if read.web_browser_for_exfile.lower() == 'firefox': 
        driver = webdriver.Firefox()
    else:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument("--window-size=1300x744")
        driver = webdriver.Chrome(chrome_options=options)

    if read.exfile_download_pref == 'regular-login':
        regular_login(url, course_folder, driver)
    elif read.exfile_download_pref == 'library-login':
        lib_login(url, course_folder, driver)
    else:
        sys.exit('Please choose between -> regular-login / library-login in settings.json')
    
    # move to the course page
    print('launching desired course page ....')
    driver.get(url)
    
    # Maximize Window if exercise-tab element not visible
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#exercise-tab")))
    driver.find_element_by_css_selector('#exercise-tab').click()
        
    # Make sure page is more fully loaded before finding the element
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "html.no-touch.member.loaded")))
    driver.find_element_by_css_selector('a > .exercise-name').click()
        
    ex_file_name = driver.find_element_by_css_selector('.exercise-name').text
    # ex_file_size = driver.find_element_by_css_selector('.file-size').text
    print('Downloading ' + ex_file_name)
    
    file_not_found = True
    while file_not_found:
        message.spinning_cursor()
        downloads_folder = install.get_path("Downloads")
        os.chdir(downloads_folder)
        for folder in os.listdir(downloads_folder):

            sys.stdout.write("\033[K")          # Clear to the end of line
            sys.stdout.write('\r{}'.format("Finding Ex_file in Downloads folder ---> " + message.return_colored_message(Fore.LIGHTYELLOW_EX,folder)))
            sys.stdout.flush()                  # Force Python to write data into terminal.

            try:
                folder = folder.decode('utf-8') # python 2.x
            except AttributeError:
                pass                            # python 3.x

            if folder == ex_file_name:
                if os.path.getsize(folder) > 0: # if file downloaded completely.
                    print('\nDownload completed.')
                    file_not_found = False
                    break
            time.sleep(0.02)                    # delay to print which file is being scanned
    try:
        shutil.move(ex_file_name, course_folder)
        print('Ex-File Moved to Course Folder successfully.')
    except:
        print('Moving error.')
    driver.close()

def lib_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/portal/patron?org=" + read.organization_url)  # launch lynda.com/signin

    # enter username
    card_number = driver.find_element_by_css_selector("#card-number")
    card_number.clear()
    card_number.send_keys(read.card_number)

    # enter password
    card_pin = driver.find_element_by_css_selector('#card-pin')
    card_pin.clear()
    card_pin.send_keys(read.card_pin)

    driver.find_element_by_css_selector('#library-login-login').click()
    print('\nlibrary card no. and card pin. entered successfully....')


def regular_login(url, course_folder, driver):
    driver.get("https://www.lynda.com/signin/")  # launch lynda.com/signin

    # enter username
    email = driver.find_element_by_css_selector("#email-address")
    email.clear()
    email.send_keys(read.username)
    driver.find_element_by_css_selector('#username-submit').click()
    print('\nusername successfully entered ....')
    # wait for password field to appear
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#password-input")))
    # enter password
    passwrd = driver.find_element_by_css_selector('#password-input')
    passwrd.send_keys(read.password)
    driver.find_element_by_css_selector('#password-submit').click()
    print('password successfully entered ....')
    time.sleep(3)
