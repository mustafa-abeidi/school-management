"""
TC4 - Admin login

Description:
    The administrator can log in and reaches the admin dashboard with
    admin-only navigation.

Steps:
    1. Open the login page.
    2. Enter username "admin" and password "admin".
    3. Click "Login".

Expected output:
    The browser is redirected to /admin_dashboard, the page heading reads
    "Admin Dashboard", and the navigation bar shows "Analytics" and "Logout".
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

    # Step 1: open the login page
    driver.get(BASE_URL + "/login")
    sleep(PAUSE)

    # Step 2: enter admin credentials
    driver.find_element(By.ID, "email").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("admin")
    sleep(PAUSE)

    # Step 3: submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/admin_dashboard"))
    sleep(PAUSE)

    # Check the expected output
    heading = driver.find_element(By.TAG_NAME, "h1").text
    nav = driver.find_element(By.CLASS_NAME, "nav-links").text
    assert heading == "Admin Dashboard", f"Unexpected heading: {heading}"
    assert "Analytics" in nav and "Logout" in nav, f"Unexpected navigation: {nav}"
    print("TC4 PASSED - admin reached the admin dashboard")
finally:
    driver.quit()
