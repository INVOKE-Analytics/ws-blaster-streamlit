from ws_blaster.manage import Manage

manage = Manage(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users', 
                option3='meniaga')


def test_get_item_in_name():
    string_names = "Ammar Azman , Ahilan Ashwin"
    n = manage.get_item_in_name(string_names)
    assert isinstance(n, str)

def test_get_list_available_unavaible_account():
    """
    TEST STILL FAILED
    KIV
    """
    option3 = manage.opt3()
    test_accs = ["file1", "file2"]
    test_path = 'D:\Desktop\INVOKE\ws_blaster\github_ws_blaster\ws-blaster-prod\chromedriver_linux64\chromedriver.exe' + str(option3) + '/'
    available = manage.get_list_available_unavaible_account(test_accs, test_path)[0]
    notavailable = manage.get_list_available_unavaible_account(test_accs, test_path)[1]

    assert isinstance(available, list)
    assert isinstance(notavailable, list)

def test_get_accs():
    accs_test_inp = ["file_1", "file_2", ".DS_Store"]
    test_accs = manage.get_accs(accs_test_inp)
    assert isinstance(test_accs, list)

def test_ws_logo():
    path = manage.ws_logo()
    assert isinstance(path, str)

def test_select_box_option1_acc_management():
    assert isinstance(manage.select_box_option1_acc_management(), list)