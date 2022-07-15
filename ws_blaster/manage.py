def opt3():
    option3 = st.selectbox('Select set of accounts to check', ('', 'meniaga','AyuhMalaysia','Burner Accounts'))
    if option3 != '':
        if option3 == 'Burner Accounts':
            option3 = 'burner'
            return option3
            