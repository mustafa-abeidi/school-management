"""
TC2 - Registration with an email that is already used

Description:
    The system refuses to create a second account with an email address
    that is already registered.

Steps:
    1. Register a student with a new email address.
    2. Open the registration page again.
    3. Register a second student using the same email address.

Expected output:
    The browser stays on the registration page and the message
    "Email already registered" is displayed.
"""

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5000"
PAUSE = 2  # seconds to pause between steps so you can watch the browser


def register(name, email):
    driver.get(BASE_URL + "/register")
    driver.find_element(By.ID, "name").send_keys(name)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    sleep(PAUSE)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.maximize_window()
    email = f"student_2@test.com"

    # Step 1: first registration (should succeed)
    register("First Student", email)
    wait.until(EC.url_contains("/login"))
    sleep(PAUSE)

    # Steps 2-3: second registration with the same email
    register("Second Student", email)
    message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert"))).text
    sleep(PAUSE)

    # Check the expected output
    assert "/register" in driver.current_url, "Browser left the registration page"
    assert message == "Email already registered", f"Unexpected message: {message}"
    print("TC2 PASSED - duplicate email was rejected")
finally:
    driver.quit()
