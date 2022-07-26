from requests import head
from ws_blaster.utils import open_driver
from ws_blaster.manage import Manage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

manage = Manage(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users')

def test_get_name():
    """
    Split new names input into a list.
    One name should not be splitted.
    """
    assert manage.get_name("Sharafi, Anis") == ['Sharafi', 'Anis']
    assert manage.get_name("Sharafi") == ['Sharafi']

def test_get_all_account_name():
    """
    Retreive all existed account (either it is banned or not)
    """
    test_fx = manage.get_all_account_name("meniaga")
    exp_output = ['Ahilan']
    assert test_fx == exp_output

def test_checking_banned_or_not():
    """
    Checking whether the account is banned or not. 
    If banned, will be appended inside not_available.
    If valid, will be appended inside available.
    """
    get_acc = manage.checking_banned_or_not("meniaga")
    test_av = ['Ahilan']
    test_not_av = []
    assert get_acc[0] == test_av
    assert get_acc[1] == test_not_av

def test_create_new_user_file():
    """
    Create new user account. 
    New user need to scan the QR code
    """
    manage.create_new_user_file('meniaga', 'Ammar')
    assert len(manage.driver_dict) == 1

def test_automatically_deleted_account_if_error():
    """
    Create account and delete the account.
    """
    manage.create_new_user_file('meniaga', 'Ammar') # create
    manage.automatically_deleted_account_if_error('meniaga', 'Ammar') # delete
    assert len(manage.account_dict) == 1

def test_taken():
    """
    Check the whether the Account in any Platform is already existed. 
    If yes, it will be in the taken-list. 
    """
    test_input = manage.get_taken('Ahilan','meniaga')
    assert test_input == ['Ahilan']

def test_take_screenshot():
    """
    Take the screenshot of the QR code.
    """
    driver = open_driver(manage.user_path)
    WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
    manage.take_screenshot(driver)
    assert len(manage.screenshot) == 1

    

