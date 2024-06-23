from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

def login_wifi(email, password, mac_address, nasid, uamip):
    # URL encode the MAC address and email
    mac_address_encoded = mac_address.replace(":", "%3A")
    email_encoded = email.replace("@", "%40")
    
    # Construct the login URL
    login_url = f"https://univillage.extremebb.net/login?res=notyet&mac={mac_address_encoded}&user={email_encoded}&userurl=&nasid={nasid}&uamip={uamip}&error=&chap-id=%24%28chap-id%29&chap-challenge=%24%28chap-challenge%29"
    
    # Set up WebDriver (make sure the path to the WebDriver executable is correct)
    driver = webdriver.Chrome()
    
    try:
        # Open the login page
        driver.get(login_url)
        
        # Wait for the email input field and fill it in (if not pre-filled)
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        email_input.clear()
        email_input.send_keys(email)
        
        # Wait for the password input field and fill it in
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.clear()
        password_input.send_keys(password)
        
        # Wait for the submit button and click it
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        submit_button.click()

        time.sleep(0.5)
        
        # Wait for the proceed button to be clickable and click it
        proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "proceed-button"))
        )
        proceed_button.click()
        
        # Check login status or perform post-login actions here
        # Example: print the current page title
        print(driver.title)
    
    finally:
        # Close the WebDriver
        driver.quit()

def check_wifi_windows():
    try:
        # Run the command 'netsh wlan show interfaces' to check Wi-Fi status
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)

        # Check if the command ran successfully
        if result.returncode == 0:
            output = result.stdout
            if "State" in output and "connected" in output:
                print("Wi-Fi is connected.")
            else:
                print("Wi-Fi is not connected.")
        else:
            print(f"Command failed with error code: {result.returncode}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    login_wifi(
        email="mubashirshoukat@gmail.com",
        password="12345678",
        mac_address="50:2F:9B:CF:55:5D",
        nasid="Univillage-Block+A",
        uamip="login.extremebb.net"
    )
    check_wifi_windows()
