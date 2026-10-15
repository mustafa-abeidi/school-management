"""
TC6 - Student cannot access the admin dashboard

Description:
    Role-based access control: a logged-in student who types the admin
    URL directly is blocked from the admin dashboard.

Steps:
    1. Register a new student and log in.
    2. Type /admin_dashboard directly into the address bar.

Expected output:
    The student is redirected to /student_dashboard and the message
    "Access denied. Admin privileges required." is displayed.
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
    email = f"student_6@test.com"

    # Step 1: register and log in as a student
    driver.get(BASE_URL + "/register")
    driver.find_element(By.ID, "name").send_keys("Access Test")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/login"))

    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/student_dashboard"))
    sleep(PAUSE)

    # Step 2: try to open the admin dashboard directly
    driver.get(BASE_URL + "/admin_dashboard")
    wait.until(EC.url_contains("/student_dashboard"))
    message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert"))).text
    sleep(PAUSE)

    # Check the expected output
    assert "/admin_dashboard" not in driver.current_url, "Student reached the admin dashboard"
    assert message == "Access denied. Admin privileges required.", f"Unexpected message: {message}"
    print("TC6 PASSED - student was blocked from the admin dashboard")
finally:
    driver.quit()
