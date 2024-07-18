#Import modules
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from funcs import element_exists, scroll_down, login_linkedin
import time 

def compscraper():
    #Get links
    links = get_clinks("PATH_TO_FILE_HERE")

    #LinkedIn Log in
    driver = login_linkedin("MailExample","PasswordExample")
    
    #Define my final DataFrame
    df_final = pd.DataFrame()

    #Initiate count
    count = 1
    #Begin loop
    for link in links:
        #Get driver to link
        driver.get(f"{link}about")
        #Sleep a while
        time.sleep(10)
        #Get Data
        df = get_data(driver, link)
        #If variable df is a str then it is an error, else I have to keep going
        if type(df) is not str:   
            #Concat to my final df if it is not my first iteration (then assign value of df to df_final to initiate)
            df_final = (pd.concat([df_final, df]))
            print("DataFrames were concatenated " + f' (i = {str(count)})')
        else:
            #Print error
            print(df + f' (i = {str(count)})')
        #Create a back up File every 50 links
        if count%50 == 0:
            df_final.to_excel(f"back_up_hasta_{str(count)}.xlsx")
        #Increment count (variable created in order to debug)
        count += 1


    #Export to Excel
    df_final.to_excel("final.xlsx")

    #Quit
    driver.quit()


#Helper functions
def get_clinks(path):
    #Load Excel
    xlsx = pd.ExcelFile(path)

    #Read Experience Sheet
    df = pd.read_excel(xlsx, "experience")

    #Obtain links
    links = np.unique(df["comp_url"].values).tolist() 

    return links

def get_data(driver, link):
        error = element_exists(driver, By.XPATH, "//*[@class='ember-view artdeco-empty-state__headline artdeco-empty-state__headline--mercado-error-server-small artdeco-empty-state__headline--mercado-spots-small']")
        if error:
            return "Sorry, this company page is outdated"
        else:
            #DATA
            #Find every data s.element (except about)
            data_elements = driver.find_elements(By.XPATH, "//*[contains(@*,'text-body-small t-black--light')]")
            #Convert them into a list of data
            data = [value.text for value in data_elements]
            #Sleep a while
            time.sleep(10)

            #COLUMNS
            #Find the s.elements of data 'titles'(excluding about)
            columns_elements = driver.find_elements(By.XPATH, "//*[contains(@*,'text-heading')]")
            #Convert them into a list of data
            columns = [column_data.text for column_data in columns_elements]
            #Create new column name if company size bigger than 1
            for index, val in enumerate(columns):
                if columns[index] == "Company size" and len(columns) != len(data):
                    columns.insert(index+1,"Active workers on LinkedIn")

            #Append link to df
            data.append(link)
            columns.append("comp_url")
            #Export DataFrame
            try:
                df = pd.DataFrame({columns[i]: [data[i]] for i in range(len(columns))})
            except:
                return "ERROR. Data lenght does not match columns lenght. Data will dismissed"
            return df

compscraper()