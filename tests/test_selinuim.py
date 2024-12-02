import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from boards.models import Board
import time
#os: Used to handle file paths, specifically for locating the chromedriver executable.
# webdriver: Provides the interface for controlling the browser.
# By: Contains different ways to locate elements on a page (e.g., by ID, name, XPath).
# Service: Used to specify the location of the ChromeDriver executable.
# WebDriverWait: A utility to wait for certain conditions to be met before continuing.
# expected_conditions as EC: Contains various conditions to wait for specific elements or actions.


@pytest.mark.django_db
def test_create_topic_automatically():
    # Set up the driver with the path to the chromedriver
    chromedriver_path = os.path.join(os.path.dirname(__file__), 'drivers', 'chromedriver.exe')
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Create a user and a board
        user = User.objects.create_user(username='zey', password='azertyuiopqs')
        board = Board.objects.create(name='django', description='This is the django board')

        # Log in the user
        driver.get('http://localhost:8000/login/')
        print("Login page loaded.")  # Debugging step
        time.sleep(2)  # Slow down the process

        username_field = driver.find_element(By.NAME, 'username')
        password_field = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys('zey')
        password_field.send_keys('azertyuiopqs')
        login_button.click()
        print("Attempting to log in.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Wait for the page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'django'))
        )
        print("Logged in successfully, board page loaded.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Navigate to the new topic page
        driver.get('http://localhost:8000/boards/3/new/')
        print("Navigated to new topic page.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Wait for fields to be visible
        subject_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'subject'))  # Field name for subject
        )
        message_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'message'))  # Field name for message
        )
        print("Subject and message fields visible.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Automatically fill in the subject and message
        subject_field.send_keys("new topic")
        message_field.send_keys("This message was created automatically using Selenium.")
        print("Filled in subject and message.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Submit the form
        submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()
        print("Submitted the form.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Wait for the new topic to appear
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Automated Topic Subject'))
        )
        print("New topic is now visible.")  # Debugging step
        time.sleep(2)  # Slow down the process

        # Verify that the new topic appears
        topic_link = driver.find_element(By.LINK_TEXT, 'Automated Topic Subject')
        assert topic_link.is_displayed(), "The topic was not created successfully."
        print("Topic created successfully.")  # Debugging step
        time.sleep(5)  # Wait for 5 seconds to allow observation

    finally:
        driver.quit()
        print("Test completed and browser closed.")  # Debugging step
