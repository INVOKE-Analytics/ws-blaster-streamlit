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
            
