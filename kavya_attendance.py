import sys
import time
import logging


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

logging.basicConfig(level='INFO', format='[%(asctime)s] %(levelname)s -- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('kavya_school')

class Attendance():  
    def __init__(self, chromedriver_path="", headless=True):
        self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        self.driver = self._get_driver(chromedriver_path=chromedriver_path, headless=headless)
        
        self.username = "CHPN_174905"
        self.password = "maintain70!"
        
        self.login_url = "https://spork.school/"

    def _get_driver(self, chromedriver_path ="", headless=True):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        if headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--ignore-certificate-errors")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'user-agent={self.headers["User-Agent"]}')
        
        executable_path = chromedriver_path if chromedriver_path else ChromeDriverManager().install()
        driver = webdriver.Chrome(executable_path,options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

        return driver
        
    def login(self):
        EMAIL_INPUT = '//input[@name="username"]'
        PASSWORD_INPUT = '//input[@name="password"]'
        LOGIN_BUTTON = '//button[@class="ui grey large fluid button responsiveSize"]'

        logger.info("Logging into school site...")
        self.driver.get(self.login_url)
        
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, EMAIL_INPUT)))
        email_input.send_keys(self.username)
        
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,PASSWORD_INPUT )))
        password_input.send_keys(self.password)
        self.driver.find_element(By.XPATH, LOGIN_BUTTON).click()
        time.sleep(5)

        if self.driver.current_url!="https://spork.school/courses/list":
            logger.info("Authentication failed!")
            sys.exit(0)
        else:
            logger.info("Logged in to the school site")
        
        logger.info("Click on schedule button...")
        #Click on schedule button 
        schedule_xpath = '//a[@class="item" and text()="Schedule"]'
        schedule_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, schedule_xpath)))
        schedule_button.click()
    
    def fill_attendance(self):
        attendance_button_xpath = '//button[@class="ui green compact button"]' # Get the xpath for the button - inspect element on page and find out
        try:
            # Wait for the attendance button to appear for 10 seconds otherwise fails
            attendance_button = WebDriverWait(self.driver, 0).until(
                EC.presence_of_element_located((By.XPATH, attendance_button_xpath)))
            attendance_button.click() # To click on the button
            return True
        except TimeoutException:
            logger.info("attendance button not available on page")
            return False
    

    def counter(self):
        now= datetime.now()
        while(int(now.strftime("%H")) <= 11):
            while(int(now.strftime("%M")) >= 15 and int(now.strftime("%M")) <= 40):
                if (self.fill_attendance()):
                    break
                time.sleep(60)
                
                 
        
if __name__=="__main__":
    at = Attendance(headless=True)
    at.login()
    at.counter()
