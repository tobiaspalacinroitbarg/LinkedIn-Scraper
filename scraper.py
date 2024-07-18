from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from funcs import element_exists, scroll_down

import time

def get_interests(driver: webdriver, category):
    buttons = None
    interests_section = None
    xpath = None

    try: # Reviso si hay sección 'interests'
        interests_section = driver.find_element(By.ID, 'interests')
        buttons = interests_section.find_elements(By.XPATH, '..//div[3]/div/button')
    except NoSuchElementException:
        return []

    # Está la categoría?
    try:
        found = False
        for button in buttons:
            if get_text_xpath(button,".//span[1]") == category:
                found = True
                button.click()
        if found == False:
            return []
    except:
        return []

    id = 'interests'
    try: # Hago click en el botón que extiende la totalidad de los resultados
        interests_section.find_element(By.XPATH, '..//div[@class="artdeco-tabpanel active ember-view"]/div/div[@class="pvs-list__footer-wrapper"]/div/a').click()
        id = 'main'
    except NoSuchElementException:
        pass
    finally:
        section = element_exists(driver, id, 3, refresh=False) # Accedo a la sección 'main' o {section} según corresponda
        if section == False:
            return False

        # Obtengo la sección - si es main busco la section correspondiente (ingresé a interests)
        # caso contrario ingreso en div id='interests'..//div[3]
        try:
            if id == 'main':
                section = section.find_element(By.XPATH, './/section')
                buttons = section.find_elements(By.XPATH, './/div[2]/div/button')
                section = section.find_element(By.XPATH, './/div[2]')
            else:
                section = section.find_element(By.XPATH, '..//div[3]')

            for button in buttons:
                if get_text_xpath(button,".//span[1]") == category:
                    button.click()
                    break
            scroll_down(driver)
        except NoSuchElementException:
            print("No encontré la sección")
            return False

        elements = []
        try:
            section = element_exists(driver, id, refresh=False)
            if section == False:
                return []
            if id == 'main':
                section = section.find_element(By.XPATH, './/section')
                section = section.find_element(By.XPATH, './/div[2]')
                xpath = './/div[@class="artdeco-tabpanel active ember-view"]/div/div/div[1]/ul/li'
            else:
                xpath = './/div[@class="artdeco-tabpanel active ember-view"]/div/ul/li'
                section = section.find_element(By.XPATH, '..//div[3]')
            elements = section.find_elements(By.XPATH, xpath)
        except Exception as e:
            print("No se encontraron los elementos o falló ")
            print(e)
            return False

        r = []
        for element in elements:
            try:
                r.append({"url":element.find_element(By.XPATH, ".//div/div/a").get_attribute("href")})
            except NoSuchElementException:
                print("No se encontró el elemento")
        return r

def get_text_xpath(element, path):
    try:
        return element.find_element(By.XPATH, path).text
    except NoSuchElementException:
        return ""

def get_user(driver: webdriver, user_url: str):
    # Abrir url ppal del user
    driver.get(user_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main")))
    except:
        driver.get(user_url)
    return driver

def get_section(driver: webdriver, section):
    parent = None
    base_general = ".//div/div[2]/div[1]"
    bases = {
        "education":base_general+"/a",
        "experience":base_general+"/div[1]",
        "languages":base_general+"/div[1]",
        "volunteering_experience":base_general+"/div[1]",
    }

    section_element = element_exists(driver, section)
    if  section_element == False:
        return [f"No posee información para {section}"]

    time.sleep(2)
    
    id = section
    try:    # Check si existen más opciones que las del inicio - hacer click en caso de existir
        section_element.find_element(By.XPATH, '..//div[@class="pvs-list__footer-wrapper"]/div/a').click()
        id='main'
    except NoSuchElementException:
        pass
    finally:
        parent = element_exists(driver, id, 5) # Accedo a la sección 'main' o {section} según corresponda
        if parent == False:
            print("No encontré la sección")
            return False
    time.sleep(3)

    try:
        elements = []
        if id == 'main': # Si ingresa a la sección porque hay más datos
            elements = parent.find_elements(By.XPATH, './/section/div[2]/div/div[1]/ul/li')
        elif id == 'about':
            return get_text_xpath(parent, '..//div[3]/div/div/div/span[1]')
        elif id == 'volunteer_causes':
            return get_text_xpath(parent, '..//div[3]/div/div/div/span[1]')
        else: # Si toma los datos desde el inicio del perfil
            elements = parent.find_elements(By.XPATH, '..//div[3]/ul/li')

        base = bases[section]
        r = []
        for element in elements:
            if section == "experience":
                nombre = get_text_xpath(element, f"{base}/div/span/span[1]")
                empleador = get_text_xpath(element, f"{base}/span[1]/span[1]")
                permanencia = get_text_xpath(element, f"{base}/span[2]/span[1]")
                ubicacion = get_text_xpath(element, f"{base}/span[3]/span[1]")
                url = element.find_element(By.XPATH, './/div/div[1]/a').get_attribute("href")
                r.append({'nombre_puesto': nombre,'empleador':empleador, 'permanencia':permanencia, 'ubicacion':ubicacion, 'url':url})
            elif section == "education":
                nombre = get_text_xpath(element, f"{base}/span[1]/span[1]")
                lugar = get_text_xpath(element, f"{base}/div/span/span[1]")
                plazo = get_text_xpath(element, f"{base}/span[2]/span[1]")
                url = element.find_element(By.XPATH, base).get_attribute("href")
                r.append({'nombre': nombre,'lugar':lugar, 'plazo':plazo, 'url':url})
            elif section == "languages":
                idioma = get_text_xpath(element, f"{base}/div/span/span[1]")
                nivel = get_text_xpath(element, f"{base}/span[1]/span[1]")
                r.append({'idioma': idioma,'nivel':nivel})
            elif section == 'volunteering_experience':
                titulo = get_text_xpath(element, f"{base}/div/span/span[1]")
                lugar = get_text_xpath(element, f"{base}/span[1]/span[1]")
                plazo = get_text_xpath(element, f"{base}/span[2]/span[1]")
                categoria = get_text_xpath(element, f"{base}/span[3]/span[1]")
                r.append({"titulo":titulo,"lugar":lugar, "plazo":plazo, "categoria":categoria})
            time.sleep(1)
    except NoSuchElementException:
        print(f"{section} - No encontré algo")
        return False
    return r

def try_section(user_driver, section):
    flag = False
    try:
        while flag == False:
            flag = get_section(user_driver, section)
    except Exception as e:
        flag = {"error": f"Error al obtener {section}"}
    return flag

def get_user_data(driver: webdriver, user_url: str):
    driver = get_user(driver, user_url)
    data = {"url":user_url}
    try:
        data["Nombre y apellido"] = driver.find_element(By.ID, "main").find_element(By.XPATH, ".//section/div[2]/div[2]/div[1]/div[1]/h1").text
    except:
        print("Falló nombre y apellido")

    print(f"Leyendo about")
    data['about'] = try_section(driver, 'about')
    
    print(f"Leyendo volunteer_causes")
    data['volunteer_causes'] = try_section(driver, 'volunteer_causes')

    for sec in ["education", "experience", "languages", "volunteering_experience"]:
        print(f"Leyendo {sec}")
        time.sleep(3)
        user_driver = get_user(driver, user_url)
        sec_data = try_section(user_driver, sec)
        data[sec] = sec_data

    data['interests'] = dict()
    for cat in ['Grupos', 'Influencers']:
        user_driver = get_user(driver, user_url)
        data['interests'][cat] = get_interests(user_driver, cat)
    return data