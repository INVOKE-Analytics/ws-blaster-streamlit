import pandas as pd
from ws_blaster.blasting import Blaster

def test_extract_from_file():
    blaster = Blaster()
    numbers = blaster.extract_from_file("tests/Sample Phone.csv")
    assert isinstance(numbers, pd.DataFrame)

test_extract_from_file()