"""
TC5 - Grade entered by the admin is visible to the student

Description:
    A grade entered by the administrator appears on the student's own
    dashboard with the correct pass/fail status.

Steps:
    1. Register a new student.
    2. Log in as admin.
    3. In "Add/Update Student Data", select the student, enter module
       "Selenium Testing", grade 14, absences 2, teacher "Dr. Smith",
       and click "Update Student Data".
    4. Log out.
    5. Log in as the student.

Expected output:
    The admin sees "Student data updated successfully!". On the student
    dashboard, the "Your Grades" table has a "Selenium Testing" row with
    grade "14.00/20" and status "Admis".
"""

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "http://localhost:5000"
PAUSE = 2  # seconds to pause between steps so you can watch the browser

from selenium.webdriver.support.ui import Select


def login(username, password):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "email").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    sleep(PAUSE)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.maximize_window()
    email = f"student_5@test.com"
    module = "Selenium Testing"

    # Step 1: register a student
    driver.get(BASE_URL + "/register")
    driver.find_element(By.ID, "name").send_keys("Grade Test")
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("/login"))

    # Step 2: log in as admin
    login("admin", "admin")
    wait.until(EC.url_contains("/admin_dashboard"))
    sleep(PAUSE)

    # Step 3: fill in and submit the grade form
    Select(driver.find_element(By.ID, "student_id")).select_by_visible_text(f"Grade Test ({email})")
    driver.find_element(By.ID, "module_name").send_keys(module)
    driver.find_element(By.ID, "grade").send_keys("14")
    driver.find_element(By.ID, "absences").send_keys("2")
    driver.find_element(By.ID, "teacher_name").send_keys("Dr. Smith")
    sleep(PAUSE)
    driver.find_element(By.XPATH, "//button[normalize-space()='Update Student Data']").click()
    admin_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "alert"))).text
    sleep(PAUSE)
    assert admin_message == "Student data updated successfully!", f"Unexpected message: {admin_message}"

    # Step 4: log out
    driver.get(BASE_URL + "/logout")
    wait.until(EC.url_contains("/login"))

    # Step 5: log in as the student
    login(email, "secret123")
    wait.until(EC.url_contains("/student_dashboard"))
    sleep(PAUSE)

    # Check the expected output
    row = driver.find_element(By.XPATH, f"//table//tr[td[normalize-space()='{module}']]")
    cells = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
    assert cells[1] == "14.00/20", f"Unexpected grade: {cells[1]}"
    assert cells[2] == "Admis", f"Unexpected status: {cells[2]}"
    print("TC5 PASSED - student sees the grade entered by the admin")
finally:
    driver.quit()
