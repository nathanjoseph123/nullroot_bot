import time
from numpy import strings
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
import sys,os,subprocess
class scraper:
    def __init__(self,url:str):

        os.environ["MOZ_DISABLE_CONTENT_SANDBOX"] = "1"
        os.environ["MOZ_DISABLE_GMP_SANDBOX"] = "1"
        os.environ["MOZ_DISABLE_RDD_SANDBOX"] = "1"
        os.environ["MOZ_DISABLE_GPU_SANDBOX"] = "1"
        
        options = Options()
        self.download_dir = "/app/downloads/"
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/firefox-esr"
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", self.download_dir)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("security.sandbox.content.level", 0)
        
        options.set_preference("app.normandy.enabled", False)
        options.set_preference("services.settings.server", "")
        options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
        options.set_preference("toolkit.telemetry.enabled", False)
        options.set_preference("browser.newtabpage.activity-stream.feeds.telemetry", False)
        options.set_preference("network.captive-portal-service.enabled", False)




        
        service = Service(log_output=sys.stdout)  # <-- prints geckodriver's real logs to Render's log stream
        subprocess.run(["pkill", "-f", "firefox"], check=False)
        subprocess.run(["pkill", "-f", "geckodriver"], check=False)
        service = Service(log_output=sys.stdout, service_args=["--marionette-port", "0"])
        self.site = webdriver.Firefox(options=options, service=service)
        self.url=url
        self.sucessful=False
        self.message={}
    def scrap(self):
        try:
            self.site.quit_on_exit=False
            self.site.get(self.url)
            self.to_do = WebDriverWait(self.site,13).until(EC.presence_of_element_located((By.CLASS_NAME, "MuiTabs-scroller.MuiTabs-fixed.css-1anid1y")))
            button=self.site.find_element(By.CLASS_NAME, "MuiTabs-scroller.MuiTabs-fixed.css-1anid1y")
            to_click =button.find_element(By.XPATH,"//button[@role='tab' and contains(., 'Mint Activity')]") 
            time.sleep(1)
            self.site.execute_script("arguments[0].click();", to_click)
            self.next=WebDriverWait(self.to_do,13).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Export CSV')]")))
        except Exception as e:
            print("errror :  ",e)
            pass

    def get_recent_minters(self):
        self.most_recent=self.next.find_element(By.XPATH,"/html/body/div/main/div/div[3]/div[3]/div[4]/div/div[2]")
        time.sleep(1)
        self.site.execute_script("arguments[0].click();", self.most_recent)
    

        self.next=self.most_recent.find_element(By.XPATH, "/html/body/div/main/div/div[3]/div[3]/div[4]/div/div[2]/div[1]/button")
        time.sleep(2)
        
        self.site.execute_script("arguments[0].click();", self.next)

        time.sleep(3)

    def get_top_minters(self):
        self.most_recent=self.next.find_element(By.XPATH,"/html/body/div/main/div/div[3]/div[3]/div[4]/div/div[1]")
        time.sleep(1)
        self.site.execute_script("arguments[0].click();", self.most_recent)

        self.next=self.most_recent.find_element(By.XPATH, "/html/body/div/main/div/div[3]/div[3]/div[4]/div/div[1]/div[1]/button")
        time.sleep(2)
        
        self.site.execute_script("arguments[0].click();", self.next)

        time.sleep(3)






