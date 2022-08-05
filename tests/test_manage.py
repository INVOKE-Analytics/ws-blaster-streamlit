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
    test_fx = manage.get_all_sim_name("meniaga")
    exp_output = ['Ahilan', 'Ammar']
    assert test_fx == exp_output

def test_get_all_platform():
    test_fx = manage.get_all_platform()
    exp_output = ['AyuhMalaysia', 'burner', 'meniaga']
    assert test_fx == exp_output

def test_checking_banned_or_not():
    """
    Checking whether the account is banned or not. 
    If banned, will be appended inside not_available.
    If valid, will be appended inside available.
    """
    get_acc = manage.checking_banned_or_not("meniaga")
    test_av = ['Ahilan', 'Ammar']
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

def test_deleted_account():
    """
    Create account and delete the account.
    """
    manage.create_new_user_file('meniaga', 'Ammar2') # create
    manage.deleted_account('meniaga', 'Ammar2') # delete
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
    TODO: Test still fail. Try tomorrow.
    Take the screenshot of the QR code.
    """
    driver = manage.create_new_user_file('meniaga', 'Ammar3') # DO NOT SCAN
    driver.maximize_window()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
    manage.take_screenshot(driver)
    driver.quit()
    manage.deleted_account('meniaga', 'Ammar3')
    assert len(manage.screenshot) == 1

def test_add_client_directory():
    manage.add_client_directory('meniaga', 'Restauran A')
    get_client_dir = manage.get_all_client_dir('meniaga')
    assert get_client_dir ==  ['Ahilan', 'Ammar', 'Restauran A']
    

