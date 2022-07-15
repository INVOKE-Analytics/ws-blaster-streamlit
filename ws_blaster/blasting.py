import re
import random
import pandas as pd

from typing import Union
from ws_blaster.utils import open_driver


class Blaster:
    def __init__(self):
        pass

    @property
    def columns(self) -> list:
        """
        Get all the columns in the passed dataframe
        """
        if isinstance(self.contacts_df, pd.DataFrame):
            return self.contacts_df.columns.tolist()
        raise TypeError("No DataFrame found")
    
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

    @staticmethod
    def clean_numbers(df: pd.DataFrame, col: str) -> list:
        '''
        Clean numbers to required format for whatsapp search

        df: Dataframe [pandas dataframe]
        col: Column name containing the numbers to blast [str]
        
        Returns dataframe with cleaned numbers
        '''
        df[col] = df[col].astype(str)
        df[col] = [re.sub("[^0-9]", "", x) for x in df[col]]
        df = df[df[col] != '']
        df[col] = ['60' + x if (x[0] == '1' and 8 < len(x) < 11) else x for x in df[col]]
        df[col] = ['6' + x if (x[0] == '0' and 9 < len(x) < 12) else x for x in df[col]]
        df[col] = ['' if (x[2] != '1' or len(x) > 12 or len(x) < 11) else x for x in df[col]]
        df = df[df[col] != '']
        df = df.drop_duplicates(subset = col)
        contact_numbers = df[col].to_list()
        return contact_numbers

    def extract_from_file(self, file):
        # TODO: Extend for other file formats
        """
        Currently only accepts csv files.
        """
        self.contacts_df = pd.read_csv(file)
        # self.contact_numbers = self.clean_numbers(self.contacts_df, phone_number_column)
        return self.contacts_df





    

