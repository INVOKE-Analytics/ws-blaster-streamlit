from os import listdir
from fastapi import status, File, UploadFile, HTTPException, APIRouter, Form, Query
from typing import List, Optional
import csv 
import codecs
import app.schemasAPI as schemas
from app.utilsAPI import SaveFile, UtilsAPI
import io
import time

from ws_blaster.blasting import Blaster
from ws_blaster.manage import Manage

router = APIRouter(
    tags=['Blasting API']
)

blast = Blaster('./User')
manage = Manage('./User')
utils = SaveFile()

@router.get('/simcard')
def get_simcard(platform:schemas.Platform):
    client_path = schemas.PlatformPath.path
    path_to_platform = client_path + '/' + platform 
    list_client = [x for x in listdir(path_to_platform)]
    list_simcard = [x for client in list_client for x in listdir(path_to_platform + '/' + client)]
    return {'simcard_name':list_simcard}

@router.get('/simcard/{id}')
def get_One_simcard(platform:schemas.Platform, id:int):
    client_path = schemas.PlatformPath.path
    path_to_platform = client_path + '/' + platform 
    list_client = [x for x in listdir(path_to_platform)]
    list_simcard = [x for client in list_client for x in listdir(path_to_platform + '/' + client)]
    return {'index': id,
        'simcard_name':list_simcard[id]}

@router.get('/getContact')
def get_contact_list():
    '''
    Get contact from database

    Example:
    SQL_QUERY = 'SELECT contact_number FROM contact_list'
    '''
    return {'status':'succeed'}

@router.post('/uploadImage')
def post_image(uploadImage:List[UploadFile]=File(...)):
    # file -- AttributeError: 'bytes' object has no attribute 'name'
    # filename -- AttributeError: 'str' object has no attribute 'name'
    # content type -- AttributeError: 'str' object has no attribute 'name'

    img = list(uploadImage)
    blast.save_files_to_blast(img)
    if blast.imgs:
        return {'status':'file uploaded'}

@router.get('/getImage')
def get_image(): 
    '''
    Get image from database.

    Example:
    SQL_QUERY = 'SELECT image FROM image_table'
    '''
    
    return {'status':'succeed'}

@router.post('/csv')
def upload_csv(upload_csv:UploadFile = File(...)):
    """
    NOTE: Testing get the csv.
    STATUS: SUCEED!
    """
    # csv_reader = csv.DictReader(codecs.iterdecode(upload_csv.file, 'utf-8'))
    # phone_number_listOfDict = [rows for rows in csv_reader]
    # phone_number_list = [number['Phone number '] for number in phone_number_listOfDict]
    # upload_csv.file.close()
    # if upload_csv is not None:
    try:
        blast.extract_from_file(upload_csv.file) 
        numbers = blast.clean_numbers('Phone number ')
        return {'list': numbers}
    except Exception as e1:
        print("ERROR 1", e1)
    

@router.post('/betablast')
def beta_blast(platform:schemas.Platform, 
                client_index:int, 
                sim_index:int, 
                message_input:str, 
                upload_img:Optional[UploadFile] = File(None),
                upload_csv:UploadFile = File(...)):      
    """
    As a the client, you need to input:
    1. The platform (specify from db)
    2. The client (choose the client bucket or directory)
    3. The simcard (choose the simcard for blasting)

    Which will be query in ORM or SQL form in the real deployment project. 
    """

    client_path = schemas.PlatformPath.path
    path_to_platform = client_path + '/' + platform 
    
    list_client = [x for x in listdir(path_to_platform)]
    if client_index > len(list_client) - 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Client on index {client_index} is out of index.')
    select_client = list_client[client_index]
    # list_simcard = [x for client in list_client for x in listdir(path_to_platform + '/' + select_client)]
    list_simcard = [x for x in listdir(path_to_platform + '/' + select_client)]
    if sim_index > len(list_simcard) - 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'Simcard on index {sim_index} is out of index.')
    
    # print("HERE", list_simcard)
    select_client = list_client[client_index]
    select_simcard = list_simcard[sim_index]

    csv_reader = csv.DictReader(codecs.iterdecode(upload_csv.file, 'utf-8'))
    phone_number_listOfDict = [rows for rows in csv_reader]
    phone_number_list = [number['Phone number '] for number in phone_number_listOfDict]
    upload_csv.file.close()

    img = upload_img
    
    return {'platform': platform, 
            'client selected': select_client, 
            'simcard selected': select_simcard,
            'list simcard': list_simcard,  
            'message input':message_input,
            'image name': img.filename,
            'image type':img.content_type, 
            'recipient phone num': phone_number_list}


@router.post('/posts/blast', status_code=status.HTTP_200_OK)
async def blast_message(
                client_index:int=0, 
                sim_index:int=0, 
                platform:str="Ayuh_Malaysia",
                message_input:List[str] = Form(...), 
                upload_img:Optional[List[UploadFile]]= File(...),
                upload_csv:UploadFile= File(...)):

    # client:str, sim_list:list, uploadImage: UploadFile):
    """
    platform (database) : platform to blast
    client (database)   : client folder to blast
    sim_list (database) : simcard list from the client folder
    """
    # print(client_path + platform)
    
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

    blast.extract_from_file(upload_csv.file) 
    numbers = blast.clean_numbers('Phone number')

    upload_csv.file.close()

    # verify simcard
    available, banned = manage.checking_banned_or_not(list_simcard,platform,select_client)

    # REQUEST BODY
    img = list(upload_img)
    blast.save_files_to_blast(img)

    # REQUEST BODY
    message = message_input
    for i in message:
        blast.add_message_variations_to_blast(i)


    print("NUMBERS", numbers)
    blast.setup_drivers_in_account(platform, select_client)
    for i, number in enumerate(numbers):
        try:
            acc, driver = blast.nav_to_number(number)
            time.sleep(5)

            print("NUMBER:", number)
            
            if blast.imgs:
                status = blast.send_file(driver)
                print("PHOTO SENT")

            # MESSAGE SEND SETUP
            message = blast.get_random_message()
            status = blast.send_message(driver, message)
            blast.apply_random_wait(i)
        except Exception as e1:
            print("ERROR SENDING:", e1)
            pass
    blast.close_drivers()
        
    print("BLASTING COMPLETE")

    #print("HERE", list_simcard, platform, select_client )
    return {'platform':platform,
            'select client':select_client, 
            'good sim':available,
            'bad sim': banned,
            'image path':blast.files_to_blast_paths}

