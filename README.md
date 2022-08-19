# ws-blaster-prod

This repo serves as the production ready version of the whats app blaster.
The module ws-blaster consists of `blasting.py`, `manage.py` and `launch.py`

## `blasting.py`

> Code related to whats app blasting

### Description

This file contains the functions that used for message blasting. 

The following is the blasting process:

1- User will upload the recipient phone number to be blasted. 
2- User can optionally choose image to be blasted.
3- User can choose the message variation to be blasted by adjusting the slider. 
4- User will write the message they want for the blasting. 
5- User will select the platform used. 
6- User wll select the client file that contained the simcard file. 
7- Once confirmed with all the details, user can click Start Blasting to start blasting the message. 

## `manage.py`

> Code related to account management.

### Description
(Accounts here is referred to simcard.)

In account management, the user can have 4 options to manage the accounts. 

1- Adding new client
    - User can add new folder that can save the Whatsapp driver folder of the simcard of the client.
    - Please use the proper name convention for the client to avoid confusion.

2- Add new simcard
    - User can add new simcard within the program. 
    - User need to scan the QR code that pop up on the screen from Whatsapp. 
    - Once scanned, the simcard has be ready for balsting.

3- Check available simcard
    - The context of available here is still linked to Whatsapp and unbanned. 
    - If the number is unlinked from the Whatsapp, or being banned, the number will be appointed as unavailable. 
    - User can check multiple simcard availability on multiple clients.

4- Delete unavailable simcard
    - Once checked the simcard availability, user can delete the unavailable simcard. 
    - Before deleting the simcard, the program will scan first the unavailable simcard, and confirmed with the user on the deletion. 
    - Once the user confirmed, user can click the delete button and the simcard will be deleted.

## `launch.py`

> Code for reusable utility functions accross files.

### Description

Based on the `blasting.py`, `manage.py` and `utils.py` functions, it will invoke within `launch.py` on respective functionality. 

Within `launch.py`, the focus is on UI that is coming from Streamlit.  

You can launch the program by writing the following command on terminal;

`python3 -m streamlit run ws_blaster/launch.py`

## `utils.py`

> Code for reusable utility functions accross files.

This file contain the function to setup the Whatsapp driver for `blasting.py` and `manage.py`. 

# TODO:

- [ ] Add documentation
- [ ] Add requirements
