from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import json
import logging
import csv

class Scraper:
    def __init__(self, email, password):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--enable-unsafe-webgl")  # For WebGL warnings
        chrome_options.add_argument("--enable-unsafe-swiftshader") 

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.email = email
        self.password = password
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='amazon_scraper.log',
            filemode='w'  
        )

    def login(self):
        try:
            self.driver.get('https://www.amazon.in')
            logging.info('Opened Amazon homepage.')

            sign_in = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'signin')]"))
            )
            sign_in.click()

            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ap_email'))
            )
            email_field.send_keys(self.email)
            self.driver.find_element(By.ID, 'continue').click()

            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ap_password'))
            )
            password_field.send_keys(self.password)
            self.driver.find_element(By.ID, 'signInSubmit').click()

            logging.info('Successfully logged in to Amazon.')
            return True

        except TimeoutException as e:
            logging.error(f'Login failed - timeout: {e}')
            return False

        except Exception as e:
            logging.error(f'Unexpected error during login: {e}')
            return False

    def get_product_link(self):
        try:
            self.driver.get('https://www.amazon.in')
            logging.info('Navigating to Amazon Best Sellers page.')

            best_sellers_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'bestsellers')]"))
            )
            best_sellers_button.click()

            elements = self.driver.find_elements(By.XPATH, "//div[@role='group']//a")
            categories = [element.get_attribute('href') for element in elements[:10] if element.get_attribute('href')]

            product_links = set()
            for category in categories:
                self.driver.get(category)
                result_links = self.driver.find_elements(By.XPATH, "//div[@id='gridItemRoot']//a")

                for link in result_links:
                    href = link.get_attribute('href')
                    if href:
                        product_links.add(href)

            return list(product_links)

        except TimeoutException:
            logging.error('Failed to fetch product links - timeout')
            return []

        except Exception as e:
            logging.error(f'Error in get_product_link: {e}')
            return []

    def data_collection(self):
        try:
            product_links = self.get_product_link()
            if not product_links:
                logging.warning('No product links found.')
                return

            product_infos = []
            for link in product_links:
                try:
                    self.driver.get(link)
                    logging.info(f'Scraping product: {link}')

                    product_info = {
                        'Name': self._safe_find_element(By.XPATH, "//div[@id='titleSection']", "N/A"),
                        'Prod_Price': self._safe_find_element(By.XPATH, "//div[@id='corePriceDisplay_desktop_feature_div']//span[@class='a-price-whole']", "N/A"),
                        'Sale_Discount': self._safe_find_element(By.XPATH, "//div[@id='corePriceDisplay_desktop_feature_div']//span[contains(@class,'savingsPercentage')]", "N/A"),
                        'Best_seller_Rating': self._safe_find_element(By.XPATH, "//div[@id='averageCustomerReviews']//span[@id='acrPopover']", "N/A"),
                        'Ship_From': self._safe_find_element(By.XPATH, "//div[@class='tabular-buybox-text' and @tabular-attribute-name='Ships from']", "N/A"),
                        'Sold_by': self._safe_find_element(By.XPATH, "//div[@class='tabular-buybox-text' and @tabular-attribute-name='Sold by']", "N/A"),
                        'Rating': self._safe_find_element(By.XPATH, "//div[@id='averageCustomerReviews']//a//span[@id='acrCustomerReviewText']", "N/A"),
                        'Product_Description': self._safe_find_element(By.XPATH, "//div[@id='feature-bullets']", "N/A"),
                        'No_bought': self._safe_find_element(By.XPATH, "//div[@id='socialProofingAsinFaceout_feature_div']", "N/A"),
                        'category_name': 'category'
                    }

                    product_infos.append(product_info)

                except Exception as e:
                    logging.error(f'Error fetching data for product {link}: {e}')

            if product_infos:
                self._save_to_csv(product_infos)

        except Exception as e:
            logging.error(f'Error in data_collection: {e}')

        finally:
            self.driver.quit()

    def _safe_find_element(self, by, value, default):
        try:
            element = self.driver.find_element(by, value)
            return element.text
        except NoSuchElementException:
            return default

    def _save_to_csv(self, data):
        csv_file = "output.csv"
        try:
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            logging.info(f'Data successfully saved to {csv_file}')
        except Exception as e:
            logging.error(f'Error saving data to CSV: {e}')

if __name__ == "__main__":
    email = input("enter enamil")
    password = input("enter password")

    amazon_bot = Scraper(email, password)
    if amazon_bot.login():
        amazon_bot.data_collection()
