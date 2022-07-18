import re
import uuid
import random
import pathlib
import pandas as pd

from ws_blaster.utils import open_driver, save_uploadedfile


class Blaster:

    def __init__(self):
        self.contacts_df = pd.DataFrame()
        self.contact_numbers = []
        self.messages = []
        self.files_to_blast_paths = []

    @property
    def columns(self) -> list:
        """
        Get all the columns in the passed dataframe
        """
        if isinstance(self.contacts_df, pd.DataFrame):
            return self.contacts_df.columns.tolist()
    
    @property
    def phone_numbers(self) -> list:
        """
        Return a list of all the phone numbers to blast to 
        """
        return self.contact_numbers
    
    @property
    def contact_numbers_info(self) -> dict:
        """
        Returns a dictionary of the number of phone numbers and a
        sample of 5 numbers
        """
        info_dict = {
            "len_phone_numbers":len(set(self.contact_numbers)),
            "sample_of_5": random.sample(self.contact_numbers, 5)
        }
        return info_dict

    def clean_numbers(self, col: str) -> list:
        """
        Clean numbers to required format for whatsapp search

        df: Dataframe [pandas dataframe]
        col: Column name containing the numbers to blast [str]
        
        Returns dataframe with cleaned numbers
        """
        self.contacts_df[col] = self.contacts_df[col].astype(str)
        self.contacts_df[col] = [re.sub("[^0-9]", "", x) for x in self.contacts_df[col]]
        self.contacts_df = self.contacts_df[self.contacts_df[col] != '']
        self.contacts_df[col] = ['60' + x if (x[0] == '1' and 8 < len(x) < 11) else x for x in self.contacts_df[col]]
        self.contacts_df[col] = ['6' + x if (x[0] == '0' and 9 < len(x) < 12) else x for x in self.contacts_df[col]]
        self.contacts_df[col] = ['' if (x[2] != '1' or len(x) > 12 or len(x) < 11) else x for x in self.contacts_df[col]]
        self.contacts_df = self.contacts_df[self.contacts_df[col] != '']
        self.contacts_df = self.contacts_df.drop_duplicates(subset = col)
        self.contact_numbers = self.contacts_df[col].to_list()
        return self.contact_numbers

    def extract_from_file(self, file):
        # TODO: Extend for other file formats
        """
        Currently only accepts csv files.
        """
        self.contacts_df = pd.read_csv(file)
    
    def save_files_to_blast(self, uploaded_files):
        """
        Saves all the uplaoded files to a `tmp` file with a 
        unique uuid
        """
        self.save_path = pathlib.Path("./tmp") / uuid.uuid1()
        self.save_path.mkdir(parents=True, exist_ok=True)
        for uploaded_file in uploaded_files:
            self.files_to_blast_paths.append(self.save_path / uploaded_file.name)
            save_uploadedfile(uploaded_file, uploaded_file.name, self.save_path)

    def message_variations_to_blast(self, message):
        self.messages.append(message)
    
    def choose_available_accounts(self):
        pass
    
    def send_message(self):
        pass





    

