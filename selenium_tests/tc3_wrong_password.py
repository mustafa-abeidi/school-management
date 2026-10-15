"""
TC3 - Login with a wrong password

Description:
    A registered student cannot log in with an incorrect password.

Steps:
    1. Register a student with a new email address.
    2. Open the login page.
    3. Enter the correct email and a wrong password.
    4. Click "Login".

Expected output:
    The browser stays on the login page, the message
    "Invalid email or password" is displayed, and no Logout link appears.
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
    email = f"student_3@test.com"

    # Step 1: register a student
    driver.get(BASE_URL + "/register")
    driver.find_element(By.ID, "name").send_keys("Login Test")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/login"))
    sleep(PAUSE)

    # Steps 2-3: open login and enter a wrong password
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("wrong-password")
    sleep(PAUSE)

    # Step 4: submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert"))).text
    sleep(PAUSE)

    # Check the expected output
    assert "/login" in driver.current_url, "Browser left the login page"
    assert message == "Invalid email or password", f"Unexpected message: {message}"
    assert not driver.find_elements(By.LINK_TEXT, "Logout"), "User appears to be logged in"
    print("TC3 PASSED - wrong password was rejected")
finally:
    driver.quit()
