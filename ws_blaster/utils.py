import os 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def save_uploadedfile(uploadedfile, file_name, path):
    '''
    Save uploaded file to path directory

    uploadedfile: Uploaded file
    file_name: File name of the uploaded file
    path: Path directory on where to save the file
    '''
    with open(os.path.join(path,file_name),"wb") as f:
        f.write(uploadedfile.getbuffer())


def open_driver(user_path, headless = True):
    '''
    Opens chromedriver and initialize Whatsapp web

    user_path: Path where user credentials are located
    headless: Decides whether to run on headless mode or otherwise

    Returns a chromedriver instance
    '''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(user_path)
    chrome_options.add_argument("--disable-notifications")
    if headless:
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--headless")
        # Specify user-agent to allow headless mode
        chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://web.whatsapp.com/')
    driver.execute_script("window.onbeforeunload = function() {};")
    return driver