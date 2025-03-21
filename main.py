from utils.selenium_setup import get_driver
from utils.email_utils import send_email
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import sys
import re
import os

load_dotenv()

LOGIN_URL = os.getenv('LOGIN_URL')
PO_URL = os.getenv('PO_URL')
PAYMENT_PASSCODE = os.getenv('PAYMENT_PASSCODE')

def main():
    driver = get_driver() #init driver

    #selenium shortcuts
    short_wait = WebDriverWait(driver, 10)
    long_wait = WebDriverWait(driver, 30)

    def short_wait(by, value, short_wait=short_wait):
        return short_wait.until(EC.element_to_be_clickable((by, value)))
    
    def long_wait(by, value, long_wait=long_wait):
        return long_wait.until(EC.element_to_be_clickable((by, value)))

    try:
        #nav to login page & login
        driver.get(LOGIN_URL)
        time.sleep(5)

        login_field = long_wait(By.ID, 'loginForm_loginName')
        login_field.send_keys(os.getenv('USERNAME'))

        pass_field = short_wait(By.ID, 'loginForm_password')
        pass_field.send_keys(os.getenv('PASSWORD'))

        login_btn = short_wait(By.CLASS_NAME, 'login-button')
        login_btn.click()
        time.sleep(5)
    except Exception as e:
        print('login failed', e)
        driver.quit()
        sys.exit(0)

    #nav to page to pay for orders
    driver.get(PO_URL)
    print('nav to order page')
    time.sleep(5)

    body_text = driver.find_element(By.TAG_NAME, 'body').text
    if 'awaiting payment' not in body_text.lower():
        print('no unpaid orders found, quitting')
        driver.quit()
        sys.exit(0)
    else:
        print('found unpaid orders, proceeding to payment flow')
        time.sleep(2)

    # select all the orders on the page and scrape the order totals
    checkbox = long_wait(By.XPATH, "//div[contains(@class, 'patch-operate')]//span[text()='Select All']")
    checkbox.click()

    selected_text_element = short_wait(By.XPATH, "//div[contains(@class, 'patch-operate')]//span[contains(text(),'Orders Selected')]")
    total_selected_text = selected_text_element.text

    orders_match = re.search(r'(\d+)', total_selected_text)
    number_selected = orders_match.group(1)
    print(f"number of orders selected: {number_selected}")

    grand_total_amount_text_el = driver.find_element(By.CLASS_NAME, 'total-amount')
    grand_total_amount_text = grand_total_amount_text_el.text

    grand_total_match = re.search(r'(\d+(?:\.\d+)?)', grand_total_amount_text)
    grand_total_number = grand_total_match.group(1)
    print(f"selected orders grand total: {grand_total_number}")

    # proceeed to checkout
    proceed_to_pay_btn = short_wait(By.CSS_SELECTOR, ".ant-btn.ant-btn-primary.patch-btn")
    proceed_to_pay_btn.click()

    # select the doba pay option
    doba_pay_btn = long_wait(By.XPATH, '//div[contains(@class, "option")]//span[text()="Doba Credit"]')
    doba_pay_btn.click()
    time.sleep(2)

    #input the payment passcode and submit
    payment_passcode_el = driver.find_element(By.CSS_SELECTOR, 'div.payment-password input')
    payment_passcode_el.send_keys(PAYMENT_PASSCODE)
    time.sleep(2)

    submit_btn = short_wait(By.CSS_SELECTOR, '.ant-btn.ant-btn-primary.ant-btn-lg')
    submit_btn.click()

    # verify the payments were successful
    payment_success_msg_el = long_wait(By.CLASS_NAME, 'success-msg')
    payment_sucess_msg = payment_success_msg_el.text
    print(payment_sucess_msg)

    #send email summary
    subject = 'DobaBot Order Summary'
    body = f"DobaBot ran successfully and paid for {number_selected} orders for a total of ${grand_total_number}"
    send_email(subject, body)

    driver.quit()

if __name__ == '__main__':
    main()