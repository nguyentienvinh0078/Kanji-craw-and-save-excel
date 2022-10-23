import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Driver():
    def  __init__(self):
        pass

    def init_driver(self, opt='hide'):
        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=3')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_argument("disable-popup-blocking")
        options.add_argument("disable-notifications")

        if opt == 'hide':
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
        if opt == 'diswin':
            options.add_argument("--window-position=-10000,0")
        elif opt == 'headless':
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        
        options.add_experimental_option ("prefs", {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
        })

        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=options) 
        return driver

    def scroll_driver(self, driver):
        scroll_pause_time = 2
        last_scroll_height = 0
        while True:
            new_scroll_height = driver.execute_script('return document.body.scrollHeight')
            if new_scroll_height != last_scroll_height:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(scroll_pause_time)
                last_scroll_height = new_scroll_height  
            else:
                break

    def get_video_src_all(self,user_home_page_url, type_hide='hide'):
        print('Crawling.........')
        driver = self.init_driver(type_hide)
        driver.get(user_home_page_url)  

        for __ in range(3):
            try:
                background_image_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div/div[2]/img[1]'))
                    )
                time.sleep(1)
                driver.refresh()
            except:
                time.sleep(1)
                break

        self.scroll_driver(driver)

        video_elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div')
        video_src_list = []
        number_of_url = len(video_elements)
        print('Total url: ', number_of_url)
        for i in range(1, number_of_url + 1):
            real_url_element = driver.find_elements(By.XPATH, f'/html/body/div[2]/div[2]/div[2]/div/div[2]/div[2]/div/div[{i}]/div[1]/div/div/a')
            for a_tag in real_url_element:
                real_url  = a_tag.get_attribute('href')
                video_src_list.append(real_url)
                print(f'{i:>2} : {real_url}')

        driver.quit()

        return video_src_list