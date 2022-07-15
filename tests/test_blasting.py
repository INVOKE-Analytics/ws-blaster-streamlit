import pandas as pd
from ws_blaster.blasting import Blaster

blaster = Blaster()

def test_extract_from_file():
    numbers = blaster.extract_from_file("tests/Sample Phone.csv")
    assert isinstance(numbers, pd.DataFrame)

def test_columns():
    columns = blaster.columns
    assert isinstance(columns, list)
