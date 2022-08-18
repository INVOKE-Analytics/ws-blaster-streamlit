import pytest
import pandas as pd
from ws_blaster.blasting import Blaster

blaster = Blaster(
    user_path="./Users")


def pytest_namespace():
    """Save variables to be used between tests"""
    return {'driver': None, 'acc': None}


def test_extract_from_file():
    """Extract the table form the user into a pandas DataFrame"""
    blaster.extract_from_file("tests/Sample Phone.csv")
    assert isinstance(blaster.contacts_df, pd.DataFrame)


def test_columns():
    """Test to check if all the columns form the dataframe were listed"""
    columns = blaster.columns
    assert isinstance(columns, list)


def test_clean_numbers():
    """Test to check if the phone numbers were transformed into the right format"""
    column = "Phone"
    numbers = blaster.clean_numbers(column)
    assert numbers == ['60125303532']


def test_setup_drivers_in_account():
    blaster.setup_drivers_in_account("AyuhMalaysia")
    assert len(blaster.driver_dict) == 1


def test_nav_to_number():
    # TODO : write a test to check that selenium went to the right number
    acc, driver = blaster.nav_to_number('0125303532')
    pytest.acc, pytest.driver = acc, driver


def test_check_if_unavailable():
    # TODO: write test to check if the account becomes unavailable
    acc = pytest.acc
    is_unavailable = blaster.check_if_unavailable(acc)
    assert is_unavailable == False


def test_send_message():
    # TODO: write a test to check that the message was sent
    driver, acc = pytest.driver, pytest.acc
    blaster.send_message(driver, 'hello')


def test_send_pic():
    # TODO: write a test to check that the files were sent
    driver, acc = pytest.driver, pytest.acc
    blaster.send_file(
        driver, "/mnt/c/Users/ahila/Programs/ws-blaster-prod/images/invoke_logo.jpg")


def test_close_drivers():
    blaster.close_drivers()
