import re
import time
import random
import pathlib
import pyperclip
import pandas as pd

from os import listdir
from ws_blaster.utils import open_driver, save_uploadedfile

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class Blaster:

    def __init__(self, user_path):
        self.user_path = pathlib.Path(user_path)
        self.contacts_df = pd.DataFrame()
        self.contact_numbers = []
        self.messages = []
        self.files_to_blast_paths = []
        self.driver_dict = {}
        self.sent = 0
        self.unavailable_accounts = []

    @property
    def columns(self) -> list:
        """
        Get all the columns in the passed dataframe.
        """
        if isinstance(self.contacts_df, pd.DataFrame):
            return self.contacts_df.columns.tolist()

    @property
    def get_num_drivers(self) -> str:
        """
        Returns the number of drivers still available.
        """
        return f"{len(self.driver_dict)} drivers remaining"

    @property
    def phone_numbers(self) -> list:
        """
        Returns a list of all the phone numbers to blast to.
        """
        return self.contact_numbers

    @property
    def contact_numbers_info(self) -> dict:
        """
        Returns a dictionary of the number of phone numbers and a sample of 5 numbers.
        """
        k = min(5, len(set(self.contact_numbers)))
        info_dict = {
            "len_phone_numbers": len(set(self.contact_numbers)),
            "sample_phone_numbers": random.sample(self.contact_numbers, k)
        }
        return info_dict

    @property
    def imgs(self):
        """
        Returns the list of images in blaster class
        """
        return self.imgs

    @property
    def blocked_accounts(self) -> list:
        """
        Returns a list of accounts that got banned during blasting.
        """
        return self.unavailable_accounts

    def get_random_message(self):
        """
        Returns a random message from all variations
        """
        return random.choice(self.messages)

    def clean_numbers(self, col: str) -> list:
        """
        Clean numbers to required format for whatsapp search

        col: Column name containing the numbers to blast [str]

        Returns dataframe with cleaned numbers
        """
        self.contacts_df[col] = self.contacts_df[col].astype(str)
        self.contacts_df[col] = [re.sub("[^0-9]", "", x)
                                 for x in self.contacts_df[col]]
        self.contacts_df = self.contacts_df[self.contacts_df[col] != '']
        self.contacts_df[col] = [
            '60' + x if (x[0] == '1' and 8 < len(x) < 11) else x for x in self.contacts_df[col]]
        self.contacts_df[col] = [
            '6' + x if (x[0] == '0' and 9 < len(x) < 12) else x for x in self.contacts_df[col]]
        self.contacts_df[col] = ['' if (x[2] != '1' or len(
            x) > 12 or len(x) < 11) else x for x in self.contacts_df[col]]
        self.contacts_df = self.contacts_df[self.contacts_df[col] != '']
        self.contacts_df = self.contacts_df.drop_duplicates(subset=col)
        self.contact_numbers = self.contacts_df[col].to_list()
        return self.contact_numbers

    def extract_from_file(self, file) -> None:
        # TODO: Extend for other file formats
        """
        Currently only accepts csv files.
        """
        self.contacts_df = pd.read_csv(file)

    def save_files_to_blast(self, uploaded_files) -> None:
        """
        Saves all the uploaded files to a `tmp` file with a unique uuid
        """
        self.save_path = pathlib.Path("./tmp")
        self.save_path.mkdir(parents=True, exist_ok=True)
        for uploaded_file in uploaded_files:
            self.files_to_blast_paths.append(
                self.save_path / uploaded_file.name)
            save_uploadedfile(
                uploaded_file, uploaded_file.name, self.save_path)

    def add_message_variations_to_blast(self, message) -> None:
        """
        Append all the variations of a message to send to a list to be used later.
        """
        self.messages.append(message)

    def setup_drivers_in_account(self, platform, headless=False) -> None:
        """
        Load the driver for all whats app accounts under platform
        """
        self.driver_path = self.user_path / platform
        for acc in listdir(self.driver_path):
            data_dir = "user-data-dir=" + str(self.driver_path / acc)
            print(data_dir)
            driver = open_driver(data_dir, headless=headless)
            self.driver_dict[acc] = driver
            time.sleep(10)

    def nav_to_number(self, phone_number, sleep=5) -> None:
        """
        Navigate to the given URL and open a chat for a given phone number
        Returns the account name and the driver for that account
        """
        acc = random.choice(list(self.driver_dict.keys()))
        driver = self.driver_dict[acc]
        url = 'https://web.whatsapp.com/send?phone=' + str(phone_number)
        driver.get(url)
        driver.execute_script("window.onbeforeunload = function() {};")
        time.sleep(sleep)
        return acc, driver

    def _select_elm(self, driver, xpath, wait):
        """
        Get the selenium object associated with the element in the DOM Tree
        """
        elm = WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
        return elm

    def send_file(self, driver, file_path, sleep=2) -> None:
        """
        Send the requested files in the chat 
        Raises a selenium.common.exceptions.TimeoutException Message if 
        it can't find the element
        """
        self._select_elm(driver, "//span[@data-testid='clip']", 300).click()
        driver.find_element(
            By.CSS_SELECTOR, "input[type='file']").send_keys(file_path)
        self._select_elm(driver, '//*[@class="_165_h _2HL9j"]', 5).click()
        time.sleep(sleep)
        return 'sent'

    def send_message(self, driver, message, sleep=2) -> None:
        """
        Send the message in the chat
        Raises a selenium.common.exceptions.TimeoutException Message if 
        it can't find the element
        """
        # Debug this in headless mode
        driver.get_screenshot_as_file("screenshot1.png")
        self._select_elm(
            driver, "//p[@class='selectable-text copyable-text']", 300).click()
        pyperclip.copy(message)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys(
            'v').key_up(Keys.CONTROL).perform()
        time.sleep(sleep)
        driver.get_screenshot_as_file("screenshot2.png")
        self._select_elm(driver, "//span[@data-testid='send']", 5).click()
        driver.get_screenshot_as_file("screenshot3.png")
        return 'sent'

    def check_if_unavailable(self, acc) -> bool:
        """
        Check if the number is unavailable in the chat 
        """
        driver = self.driver_dict[acc]
        elm = driver.find_elements(
            by=By.PARTIAL_LINK_TEXT, value='Need help to get started?')
        elm_is_present = bool(len(elm) > 0 and elm[0].is_displayed())
        return elm_is_present

    def remove_driver(self, acc) -> str:
        """
        Remove the driver if the driver becomes unavailable
        """
        # TODO: Add logging
        driver = self.driver_dict[acc]
        driver.quit()
        del self.driver_dict[acc]
        self.unavailable_accounts.append(self.driver_path / acc)
        return acc
        # st.subheader('*** Driver-- ' + str(driver_ls[drivers_idx]) + ' is unavailable ***')
        # st.subheader('*** Drivers left: ' + str(driver_count) + ' ***')
        # st.subheader('### ALL ACCOUNTS ARE CURRENTLY UNAVAILABLE! BLASTING STOPPED AT INDEX: ' + str(i) + '###')

    def apply_random_wait(self, count) -> None:
        """
        Apply some random wait time to lower the risk of accounts gettig banned
        """
        if count % 300 == 0 and count != 0:
            time.sleep(random.randint(500, 1000))
        elif count % 10 == 0 and count != 0:
            time.sleep(random.randint(5, 10))
            # return 'Numbers gone through: ' + str(count) + ', Messages sent: ' + str(count)
        else:
            time.sleep(random.randint(2, 5))

    def close_drivers(self) -> None:
        """
        Close all open drivers once blasting has completed.
        """
        for driver in self.driver_dict.values():
            driver.quit()
