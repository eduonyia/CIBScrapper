from typing import List, Dict, Any
from log import load_logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class CIBScrapper:
    def __init__(self, cib_website, test=True):
        # load logger
        self.logger = load_logging(__name__)

        # create empty list to store an array of dicts
        self.sn = []
        self.name = []
        self.staff = []
        self.staff_position = []
        self.address = []
        self.website = []

        self.current_page = 1
        self.test = test

        if self.test is True:
            try:
                self.logger.info(f"Chartered Institute  of Banker's data scrapping has started...")
                self.driver = webdriver.Chrome()
                self.driver.get(cib_website)
            except Exception:
                self.logger.error("An error occurred opening the Chartered Institute  of Banker webpage", exc_info=True)
        else:
            try:
                self.logger.info(f"Chartered Institute  of Banker's data scrapping has started...")
                options = Options()
                options.headless = True

                self.driver = webdriver.Chrome(options=options)
                self.driver.get(cib_website)

            except Exception:
                self.logger.error("An error occurred opening the Chartered Institute  of Banker webpage", exc_info=True)

    def scrape_cib_data(self) -> Dict[str, List[Any]]:
        while True:
            # page_table = self.get_page_table()
            # page_body = self.get_table_body(page_table)
            #
            # # get all view button along with their associated attributes
            # page_rows = self.get_page_rows(page_body)

            self.sn = self.get_sn()
            self.name = self.get_name()
            self.staff = self.get_staff()
            self.staff_position = self.get_staff_position()
            self.address = self.get_address()
            self.website = self.get_website()

            if self.test is True:  # for testing purposes only scrapes 5 pages worth of data
                if self.current_page == 2:
                    break

            page_bool = self.get_next_page()

            if page_bool is False:
                break

        full_data = {
            "name": self.name, "staff": self.staff, "staff_position": self.staff_position,
            "address": self.address, "website": self.website
        }

        #  "sn": self.sn removed

        return full_data

    def get_next_page(self) -> bool:
        pagination = self.driver.find_element(By.CLASS_NAME, "pagination")
        try:
            next_page = pagination.find_element(By.LINK_TEXT, '›')

            next_page.click()
            self.current_page += 1
            return True
        except NoSuchElementException:
            self.logger.info("End of Bankers  data pages")
            return False

    def get_total_element(self) -> int:
        total_element = len(self.driver.find_elements(By.XPATH,
                                                      '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr'))
        return total_element

    def get_sn(self) -> List:
        row_num = 1
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            self.logger.info(f"page:{self.current_page}, row:{row_num}")
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[1]')
            for element in w:
                self.sn.append(element.text)

            row_num += 1

        return self.sn

    def get_name(self) -> List:
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[2]')
            for element in w:
                self.name.append(element.text)

        return self.name

    def get_staff(self) -> List:
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[3]')
            for element in w:
                self.staff.append(element.text)

        return self.staff

    def get_staff_position(self) -> List:
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[4]')
            for element in w:
                self.staff_position.append(element.text)

        return self.staff_position

    def get_address(self) -> List:
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[5]')
            for element in w:
                self.address.append(element.text)

        return self.address

    def get_website(self) -> List:
        total_element = self.get_total_element()
        for i in range(1, total_element + 1):
            w = self.driver.find_elements(By.XPATH,
                                          '//*[@id="app"]/main/section[3]/div/div/div[2]/div/div/div/div[2]/table/tbody/tr[' + str(
                                              i) + ']/td[6]')
            for element in w:
                self.website.append(element.text)

        return self.website
