def get_profile_links():  
    #Importo librerías
    import pandas as pd
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import time 

    #Importo funciones
    def scroll_down(driver: webdriver):
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def element_exists(driver:webdriver, by:By, ref:str, time=4, refresh=False):
        ret = False
        try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
            ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
            if refresh == True:
                driver.refresh()
            try:
                ret = WebDriverWait(driver, time).until(EC.presence_of_element_located((by,ref)))
            except :
                pass
        except TimeoutException:
            pass
        return ret

    def log_in(email, password):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.linkedin.com/")
        time.sleep(10)
        element_exists(driver, By.XPATH,'//*[@id="session_key"]').send_keys(email)
        element_exists(driver, By.XPATH,'//*[@id="session_password"]').send_keys(password)
        time.sleep(10)
        element_exists(driver, By.XPATH,'//*[@class="sign-in-form__submit-button"]').click()
        time.sleep(10)
        return driver

    def load_users(path):
        df = pd.read_excel(path)
        userslist = (df["First Name"] + ' ' + df["Last Name"]).to_list()
        return userslist

    def load_locations(path):
        df = pd.read_excel(path)
        locationlist = df["Primary City"].to_list()
        return locationlist

    def choose_user(df, data, links, user):
        userslocation = df["Primary City"].to_list()
        usersuniversity = df["Organization Name"].to_list()
        userstitle = df["Title"].to_list()
        maxcount = 0
        userindex = "x"
        for i in range(len(data)):
            count = 0
            if user in data[i]:
                count+=1
            if userslocation[i] in data[i]:
                count+=1
            if usersuniversity[i] in data[i]:
                count+=1
            if userstitle[i] is str and userstitle[i] in data[i]:
                    count+=1
            if count>maxcount:
                maxcount = count
                userindex = i
            elif count == maxcount:
                if type(userindex) is list:
                    userindex = userindex + [i]
                else:
                    userindex = [userindex] + [i]
        return userindex

    def get_links():
        for user in userslist:
            time.sleep(5)
            searchinput = user + ' WORD' #INPUT 1
            driver.get(f"https://www.linkedin.com/search/results/people/?keywords={searchinput}")
            time.sleep(3)
            if element_exists(driver, By.XPATH,'//*[@class="reusable-search-filters__no-results artdeco-card mb2"]'):
                time.sleep(5)
                searchinput = user + ' WORD 2'#INPUT 2
                driver.get(f"https://www.linkedin.com/search/results/people/?keywords={searchinput}")
                time.sleep(3)
            if element_exists(driver, By.XPATH,'//*[@class="reusable-search-filters__no-results artdeco-card mb2"]'):
                    time.sleep(5)
                    searchinput = user + ' WORD 3'#INPUT 3
                    driver.get(f"https://www.linkedin.com/search/results/people/?keywords={searchinput}")
                    time.sleep(3)
            if element_exists(driver, By.XPATH,'//*[@class="reusable-search-filters__no-results artdeco-card mb2"]'):
                    time.sleep(5)
                    searchinput = user + 'WORD 4'#INPUT 4
                    driver.get(f"https://www.linkedin.com/search/results/people/?keywords={searchinput}")
                    time.sleep(3)
            if element_exists(driver, By.XPATH,'//*[@class="reusable-search-filters__no-results artdeco-card mb2"]'):
                        print(f"{user} has no link")
                        continue
            lelements = driver.find_elements(By.XPATH, '//*[@class="app-aware-link  scale-down "]')
            links = [element.get_attribute('href') for element in lelements]
            delements = driver.find_elements(By.XPATH, '//*[@class="reusable-search__result-container"]')
            data = [item.text for item in delements]
            userindex = choose_user(pd.read_excel(filepath), data, links, user)
            if userindex != "x":
                if type(userindex) is list:
                    linksfinal.append(links[subindex] for subindex in userindex)
                    print(f"{user} links added")
                else:
                    linksfinal.append(links[userindex])
                    print(f"{user} link added")
            else:
                print(f"{user} has no link")
        print("Exporting links.txt file")
        output_file = open('output.txt', 'w')
        for link in linksfinal:
            output_file.write(str(link) + "," +'\n')
        output_file.close()

    #### CHANGE HERE ##
    email = "MAIL_EXAMPLE"
    password = "PASSWORD_EXAMPLE"
    filepath = "Parliamentors\Alumni.xlsx"
    ##### CHANGE HERE ####

    linksfinal = []
    driver = log_in(email, password)
    userslist = load_users(filepath)
    locationlist = load_locations(filepath)
    get_links()
    return
