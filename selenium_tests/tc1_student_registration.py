"""
TC1 - Student registration

Description:
    A new student can create an account from the registration page.

Steps:
    1. Open the registration page (/register).
    2. Enter a full name, a new email address and a password.
    3. Click "Register".

Expected output:
    The browser is redirected to the login page and the message
    "Registration successful! Please login." is displayed.
"""
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5000"
PAUSE = 2  # seconds to pause between steps so you can watch the browser


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.maximize_window()
    email = f"student_1@test.com"

    # Step 1: open the registration page
    driver.get(BASE_URL + "/register")
    sleep(PAUSE)

    # Step 2: fill in the form
    driver.find_element(By.ID, "name").send_keys("Test Student")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    sleep(PAUSE)

    # Step 3: submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/login"))
    message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert"))).text
    sleep(PAUSE)

    # Check the expected output
    assert "/login" in driver.current_url, "Not redirected to the login page"
    assert message == "Registration successful! Please login.", f"Unexpected message: {message}"
    print("TC1 PASSED - student registered and redirected to login")
finally:
    driver.quit()
