from fastapi import status, HTTPException, APIRouter, BackgroundTasks
from typing import Optional
import app.schemasAPI as schemas
from os import listdir
from starlette.responses import FileResponse
from app.utilsAPI import UtilsAPI
import ws_blaster.utils as utils
from ws_blaster.manage import Manage

import time
from threading import Timer

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



router = APIRouter(
    tags=['Account Management API']
)
manage = Manage('./User')
utilsAPI = UtilsAPI()


@router.post('/posts/client')
def add_new_client(platform:str, client:str):
    '''
    Add new client directory to WSB database.

    NOTE: API SUCCEED!
    '''
    manage.add_client_directory(platform, client)
    return {'status': f'{client} directory successfull added!'}

@router.post('/posts/simcard')
def add_new_simcard( new_simcard:str, 
                    background_task:BackgroundTasks, 
                    client:str="growthhack", 
                    platform:str="Ayuh_Malaysia"):
    '''
    Add new simcard to WSB database.

    NOTE: NOT SUCCEED. CANNOT BE SCANNED DIRECTLY FROM API
    ONLY CAN BE SCAN FROM LOCAL.
    '''
    try:
        
        driver = manage.create_new_user_file(platform,
                                            client,
                                            new_simcard)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                    '//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')))
        time.sleep(5)
        manage.take_screenshot(driver)
        print("SCREENSHOT TAKEN")
        qr_screenshot = FileResponse('/home/ammar/wsbAPI/venvWSBAPI/wsb_api/screenshot/QR_code_1.png')
        
        #func_wait(driver, 60)
        WebDriverWait(driver, 120).until(EC.visibility_of_element_located((By.XPATH,
                                            '//*[@title="Search input textbox"]')))
        print("STATUS ENDED")
        return {'status':'ss generated.Go scan'}
    except Exception as e1:
        print("ERROR", e1)

@router.delete('/delClient')
def delete_client():
    '''
    Delete client directory from database.
    '''
    return {'status':'succeed'}

@router.delete('/delSimcard')
def delete_simcard(platform:str, client:str, simcard:str):
    '''
    Delete simcard directory from database

    NOTE: API SUCCEED!
    '''
    manage.deleted_account(platform, client, simcard)
    return {'status':f'Simcard {simcard} has been deleted.'}

@router.post('/verify', status_code=status.HTTP_200_OK)
def verify_simcard(client_index:int, 
                sim_index:int, 
                platform:str="Ayuh_Malaysia"):

    """
    NOTE: API SUCEED!
    """

    client_path = schemas.PlatformPath.path
    path_to_platform = client_path + '/' + platform 
    
    list_client = [x for x in listdir(path_to_platform)]
    if client_index > len(list_client) - 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Client on index {client_index} is out of index.')

    select_client = list_client[client_index]
    list_simcard = [x for x in listdir(path_to_platform + '/' + select_client)]
    if sim_index > len(list_simcard) - 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Simcard on index {sim_index} is out of index.')
    
    # print("HERE", list_simcard)
    select_client = list_client[client_index]
    select_simcard = list_simcard[sim_index]

    # verify simcard
    available, banned = manage.checking_banned_or_not(list_simcard,platform,select_client)

    print("HERE", list_simcard, platform, select_client)
    return {'platform':platform,
            'list client':list_client,
            'list simcard':list_simcard,
            'select client':select_client, 
            'available':available,
            'nonavailable': banned}