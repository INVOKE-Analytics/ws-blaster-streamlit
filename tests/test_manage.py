from ws_blaster.manage import Manage

manage = Manage()

def test_remove_DS_store():
    assert isinstance(manage.remove_DS_store('DS store path to the file'), list)

def test_account_collection():
    test_available = manage.account_collection[0]
    test_non_available = manage.account_collection[1]

    assert(test_available, list)
    assert(test_non_available, list)