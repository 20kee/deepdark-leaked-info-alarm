from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import json
class Driver:
    def __init__(self):
        self.driver = None
        self.str_to_by = {
            "class" : By.CLASS_NAME,
            "name"  : By.NAME,
            "tag"   : By.TAG_NAME, 
            "id"    : By.ID
        }

    def driver_init(self):
        chrome_options = Options()
        service = Service(ChromeDriverManager().install())

        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('disable-gpu')
        #chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('ignore-certificate-errors')
        chrome_options.add_argument('hide-scrollbars')
        chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel MAc OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.set_page_load_timeout(600)

class Crawling(Driver):
    def __init__(self, webs_json) -> None:
        super().__init__()
        self.webs = dict()
        self.webs_json = webs_json

    def get_from_json(self) -> None:
        with open(self.webs_json) as f:
            self.webs = json.load(f)
        
    def crawl(self):
        self.driver_init()
        new_leaked_infos = dict()
        for site_name, site_info in self.webs.items():
            new_leaked_infos[site_name] = []
            try:
                print(site_name, '접속')
                site_url = site_info['url']
                self.driver.get(site_url)
                time.sleep(10)
                selectors = site_info['selector']
                already_leaked_infos = site_info['leaked']
                titles = self.get_titles(selectors)
                #print(titles)
                for title in titles:
                    if title not in already_leaked_infos:
                        new_leaked_infos[site_name].append(title)
                
                already_leaked_infos.extend(new_leaked_infos[site_name])
                self.webs[site_name]['leaked'] = already_leaked_infos
                print(site_name, '종료')
            except Exception as e:
                print("Error", e)
        self.driver.quit()
        return new_leaked_infos
        
    def get_titles(self, selectors):
        titles = None
        multi = False
        for selector in selectors:
            if selector == "multi":
                multi = True
                continue
            
            if multi:
                if titles == None:
                    titles = self.driver.find_elements(By.CSS_SELECTOR, selector)
                else:
                    try:
                        for i, element in enumerate(titles):
                            titles[i] = element.find_element(By.CSS_SELECTOR, selector)
                    except:
                        titles = titles.find_elements(By.CSS_SELECTOR, selector)
            else:
                if titles == None:
                    titles = self.driver.find_element(By.CSS_SELECTOR, selector)
                else:
                    titles = titles.find_element(By.CSS_SELECTOR, selector)
            #print(titles)
                    
        return list(map(lambda x: x.text, titles))
    
    def save_to_json(self):
        with open(self.webs_json, 'w') as f:
            json.dump(self.webs, f, indent=2)

    def main(self):
        self.get_from_json()
        new_leaked_infos = self.crawl()
        print(new_leaked_infos)
        self.save_to_json()
        return new_leaked_infos
    