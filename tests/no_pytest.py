from ws_blaster.manage import Manage
from ws_blaster.utils import open_driver
manage = Manage(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users')


#test_list = manage.get_all_platform_list_dir()

#setup_acc_driver = manage.setup_new_account(platform="meniaga", account_name="sharafi")

#test_run = Manage(user_path='')
#print(test_run.activate_WS_website())
#sharafi = 'user-data-dir=D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users\\meniaga\\sharafi'
#anis = 'user-data-dir=D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users\\AyuhMalaysia\\anis'
#open_WS = open_driver(sharafi, headless=False)

#open_WS

#open_driver(manage.setup_path_new_account('AyuhMalaysia','anis'))

print(manage.create_new_user_file('meniaga', 'Ammar'))