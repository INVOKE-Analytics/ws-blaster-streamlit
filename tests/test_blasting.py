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

# blaster.close()