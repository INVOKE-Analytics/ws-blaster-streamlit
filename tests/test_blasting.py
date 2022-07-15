from numpy import number
import pandas as pd
from ws_blaster.blasting import Blaster

blaster = Blaster()

def test_extract_from_file():
    df = blaster.extract_from_file("tests/Sample Phone.csv")
    assert isinstance(df, pd.DataFrame)

def test_columns():
    columns = blaster.columns
    assert isinstance(columns, list)

def test_clean_numbers():
    column = "Phone"
    numbers = blaster.clean_numbers(column)
    assert numbers == ['60125303532']