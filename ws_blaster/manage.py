def opt3():
    option3 = st.selectbox('Select set of accounts to check', ('', 'meniaga','AyuhMalaysia','Burner Accounts'))
    if option3 != '':
        if option3 == 'Burner Accounts':
            option3 = 'burner'
            return option3

def remove_DS_store(option3):
        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        accs = [f for f in listdir(mypath)]
        if ".DS_Store" in accs:
                accs.remove(".DS_Store")
        return accs

def account_collection(accs, option3):
    available = []
    not_available = []
    mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
    for acc in accs:
        driver = open_driver(mypath + acc)
        try:
            elems = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
            not_available.append(acc)
        except:
            available.append(acc)
        driver.quit()

    return (available, not_available)

def checking_acc_availability(available, not_available):
    if len(available) == 0:
        st.subheader('All accounts are not available!')
        return st.subheader('Unavailable accounts: ', ', '.join(not_available))
    elif len(not_available) == 0:
        st.subheader('All accounts are available!')
        return st.subheader('Available accounts: ' + str(', '.join(available)))
    else:
        st.subheader('Available account(s): ' + str(', '.join(available)))
        return st.subheader('Unavailable account(s): ' + str(', '.join(not_available)))
            
            
