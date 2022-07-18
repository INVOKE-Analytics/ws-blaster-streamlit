import pandas as pd
from ws_blaster.blasting import Blaster

blaster = Blaster(user_path="./Users")

def test_extract_from_file():
    blaster.extract_from_file("tests/Sample Phone.csv")
    assert isinstance(blaster.contacts_df, pd.DataFrame)

def test_columns():
    columns = blaster.columns
    assert isinstance(columns, list)

def test_clean_numbers():
    column = "Phone"
    numbers = blaster.clean_numbers(column)
    assert numbers == ['60125303532']

def test_setup_drivers_in_account():
    blaster.setup_drivers_in_account("meniaga")
    assert len(blaster.driver_dict) == 1

def test_nav_to_number():
    driver, acc = blaster.nav_to_number('60125303532')
    # TODO : write a test to check that selenium went to the write number

# TODO: write a function to get selenium to close the browser
# blaster.close()