import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.main import usersList
import time

def setup_browser():
    """Configure browser differently for local vs CI (GitHub Actions)"""
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):  # Running in GitHub Actions
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    else:
        # Local (assumes chromedriver is on PATH)
        return webdriver.Chrome()

# Sign Up Tests
def test_successful_signup_shows_thank_you():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("Yusuf Sharif")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)  
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        # Close alert 
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete

        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-message"))
            ).text
        assert "Thanks for Signing up" in message
        time.sleep(1)
    finally:
        driver.quit()

def test_invalid_email():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("Yusuf Sharif")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("yusufsharifhotmail.com")
        signup_email = driver.find_element(By.ID, "signup-email")
        time.sleep(1)  
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        validation_msg = driver.execute_script("return arguments[0].validationMessage;", signup_email)
        assert "Please include an '@' in the email address." in validation_msg
        time.sleep(1)
    finally:
        driver.quit()

def test_blank_password_prevents_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("Yusuf Sharif")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)  
        signup_password = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            )
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        validation_msg = driver.execute_script("return arguments[0].validationMessage;", signup_password)
        assert "Please fill out this field." in validation_msg
        time.sleep(1)
        print(usersList)  # Print usersList to verify no new user was added
    finally:
        print(usersList)  # Print usersList to verify no new user was added
        driver.quit()
        

def test_form_resets_after_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("Mohamed Ahemd")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("mohamedahemd@hotmail.com")
        time.sleep(1)  
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        # Close alert 
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete

        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-message"))
            ).text
        assert "Thanks for Signing up" in message
        
        name_value = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).get_attribute("value")
        email_value = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).get_attribute("value")
        password_value = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).get_attribute("value")
        assert name_value == ""
        assert email_value == ""
        assert password_value == ""
        time.sleep(1)
    finally:
        driver.quit()

def test_email_already_exists():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        #send the same email again
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("Mohamed Ahemd")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("mohamedahemd@hotmail.com")
        time.sleep(1)  
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        # Check for error message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-message"))
            ).text
        assert "User with this email already exists" in message
        time.sleep(1)
    finally:
        driver.quit()

#Login Tests
def test_successful_login():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete
        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Log in successful!" in message
        time.sleep(1)
    finally:
        driver.quit()

def test_login_with_wrong_email():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("invalid-user@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("wrong-password")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Check for error message
        error_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "User not found" in error_message
        time.sleep(1)
    finally:
        driver.quit()

def test_login_with_wrong_password():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("wrong-password")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Check for error message
        error_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Incorrect password" in error_message
        time.sleep(1)
    finally:
        driver.quit()

# Send Transaction Tests
def test_send_transaction_with_insufficient_balance():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        #login first
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete
        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Log in successful!" in message
        time.sleep(1)

        # Send transaction
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "amount"))
            ).send_keys("10000")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "toAccountID"))
            ).send_keys("3")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#transaction-form > button"))
            ).click()
        time.sleep(1)
        # Check for error message
        error_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "transaction-message"))
            ).text
        assert "Insufficient balance" in error_message
        time.sleep(1)
    finally:
        driver.quit()

def test_send_transaction_success():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        #login first
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete
        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Log in successful!" in message
        time.sleep(1)

        # Send transaction
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "amount"))
            ).send_keys("1")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "toAccountID"))
            ).send_keys("3")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#transaction-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        # Check for error message
        success_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "transaction-message"))
            ).text
        assert "Transaction" in success_message and "successful" in success_message
        time.sleep(1)
    finally:
        driver.quit()

#Transactions History Tests
def test_view_transactions_history():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        #login first
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("yusufsharif@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete
        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Log in successful!" in message
        time.sleep(1)

        # Send transaction
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "amount"))
            ).send_keys("5")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "toAccountID"))
            ).send_keys("3")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#transaction-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        # Check for error message
        success_message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "transaction-message"))
            ).text
        assert "Transaction" in success_message and "successful" in success_message
        time.sleep(1)

        # View transactions hisory
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "load-transactions"))
            ).click()
        time.sleep(1)
        # Wait untill spinner duisappears
        WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "transactions-spinner"))
            )
        # Check for the transactions table
        table = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, "transactions-table"))
            )
        assert table is not None
        time.sleep(1)
    finally:
        driver.quit()

def test_view_transactions_no_transactions():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000")
        wait = WebDriverWait(driver, 10)
        
        #Sign up first
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-name"))
            ).send_keys("New User")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-email"))
            ).send_keys("NewUser@hotmail.com")
        time.sleep(1)  
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#signup-form > button"))
            ).click()
        time.sleep(1)
        # Close alert 
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete

        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "signup-message"))
            ).text
        assert "Thanks for Signing up" in message
        time.sleep(1)

        #Login second
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-email"))
            ).send_keys("NewUser@hotmail.com")
        time.sleep(1)
        WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-password"))
            ).send_keys("password 123")
        time.sleep(1)
        # Submit the form
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-form > button"))
            ).click()
        time.sleep(1)
        # Close alert
        WebDriverWait(driver, 3).until(
                EC.alert_is_present()
            ).accept()
        time.sleep(1)  # Wait for the form submission to complete
        # Check for success message
        message = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "login-message"))
            ).text
        assert "Log in successful!" in message
        time.sleep(1)

        # View transactions hisory third
        WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, "load-transactions"))
            ).click()
        time.sleep(1)
        # Wait untill spinner duisappears
        wait.until(EC.invisibility_of_element_located((By.ID, "transactions-spinner")))
        # Check for the transactions table
        tables = driver.find_elements(By.ID, "transactions-table")
        assert len(tables) == 0
        time.sleep(1)
    finally:
        driver.quit()