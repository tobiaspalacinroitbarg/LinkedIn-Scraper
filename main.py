import scraper as sp
from ordenador import ordenar_datos
from get_profile_links import get_profile_links 
from funcs import login_linkedin
import json

USERNAME = "USERNAME_EXAMPLE"
PASSWORD = "PASSWORD_EXAMPLE"
INPUT = "Parliamentors\links.txt"
OUTPUT = "Parliamentors\database.json"
# Login en linkedin
driver = login_linkedin(USERNAME, PASSWORD)

# Obtener información de los usuarios
f = open(INPUT, "r",encoding="utf-8")
urls = f.readlines()
f.close()

users_data = []

i = 1
with open(OUTPUT, 'a+', encoding='utf8') as json_file:
    json_file.write("[")
    for url in urls:
        while True:
            try:
                user_data = sp.get_user_data(driver, url)
                users_data.append(user_data)
                json.dump(user_data, json_file, ensure_ascii=False)
                if i < len(urls):
                    json_file.write(",")
                    i+=1
                break
            except Exception as e:
                # TODO: agregar driver.quit() ?
                #driver = login_linkedin(USERNAME, PASSWORD)
                print(f"Error en {url} - {e}")
    json_file.write("]")
driver.quit()

ordenar_datos(OUTPUT, 'parliamentorslinkedin.xlsx')