from requests import head
from ws_blaster.utils import open_driver
from ws_blaster.manage import Manage

manage = Manage(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users')

def test_get_name():
    assert manage.get_name("Sharafi, Anis") == ['Sharafi', 'Anis']

def test_get_all_account_name():
    test_fx = manage.get_all_account_name("meniaga")
    exp_output = ['Ammar', 'sharafi']
    assert test_fx == exp_output

def test_checking_account_list_dir():
    get_acc = manage.checking_account_list_dir("meniaga")
    test_av = []
    test_not_av = ['D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users\\meniaga\\Ammar',
        'D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users\\meniaga\\sharafi']
    assert get_acc[0] == test_av
    assert get_acc[1] == test_not_av

def test_create_new_user_file():
    manage.create_new_user_file('meniaga', 'Ammar')
    assert len(manage.driver_dict) == 1

def test_automatically_deleted_account_if_error():
    # TODO: Test still FAILED
    manage.create_new_user_file('meniaga', 'Ammar')
    manage.automatically_deleted_account_if_error('meniaga', 'Ammar')
    assert len(manage.account_dict) == 1

def test_taken():
    test_input = manage.get_taken('sharafi','meniaga')
    assert test_input == ['sharafi']

    

