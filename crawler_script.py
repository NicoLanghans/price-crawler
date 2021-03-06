from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from playwright.sync_api import sync_playwright
import subprocess

i = 0                   #Initialisierung
process_control = 0

def path_def():
    p = ''
    for r, d, f in os.walk("C:\\"):
        for files in f:
            if files == "chrome.exe":
                p = os.path.join(r, files)
        if p != '':
            break
    return p


exe_path = path_def()  # Reihenfolge geändert
user_profile = os.environ['USERPROFILE']
data_dir = os.path.join(r'C:\Users', user_profile, r'AppData\Local\Google\Chrome\User Data')

with sync_playwright() as s:
    browser = s.chromium.launch(executable_path=exe_path, headless=False, slow_mo=200)  # path hinzugefügt
    page = browser.new_page()
    page.goto('http://wieistmeinuseragent.de/')
    ua_content = page.content()
    soup = BeautifulSoup(ua_content, 'lxml')
    user_agent = soup.find('p', class_='useragent').text.strip()
    browser_version = soup.findAll('p')[1].get_text(strip=True).replace("\n", " ").replace("\t", " ")

df = pd.DataFrame(
    columns=["url", "price", "inco_price", "name", "ua", "browser"])  # benoetigte dataframes initialisieren
all_prices_df = pd.DataFrame(columns=["url", "price", "inco_price", "name", "ua", "browser"])
df_input = pd.read_csv('import_url.csv')


for row in df_input.itertuples():  # csv Input den Variablen zuweisen
    url = row[1]
    pt_css_sel = row[2]
    pt_css_sel_attr = row[3]
    pt_css_sel_name = row[4]
    p_css_sel = row[5]
    p_css_sel_attr = row[6]
    p_css_sel_name = row[7]
    nt_css_sel = row[8]
    nt_css_sel_attr = row[9]
    nt_css_sel_name = row[10]
    n_css_sel = row[11]
    n_css_sel_attr = row[12]
    n_css_sel_name = row[13]
    shop = url[12:(url.find('/', 10, ))]
    price = 0
    inco_price = 0


    if i<5:             #Laufvariable für Screenshots
        i += 1
    else:
        i=1

    if process_control < 10:    #Absicherung CPU-Überlastung
        process_control += 1
    else:
        subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
        process_control = 0

    try:

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(executable_path=exe_path, user_data_dir=data_dir,
                                                           headless=False, slow_mo=3000, user_agent=user_agent)
            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=f"screenshot_{shop}_{i}.png", full_page=True)
            content = page.content()
            soup = BeautifulSoup(content, 'lxml')
            if pt_css_sel_attr == 'class':
                price_tag = soup.find(pt_css_sel, class_=pt_css_sel_name)
            elif pt_css_sel_attr == 'display':
                price_tag = soup.find(pt_css_sel, display=pt_css_sel_name)
            elif pt_css_sel_attr == 'id':
                price_tag = soup.find(pt_css_sel, id=pt_css_sel_name)

            if p_css_sel_attr == 'class':
                price = price_tag.find(p_css_sel, class_=p_css_sel_name).text.strip()
            elif p_css_sel_attr == 'id':
                price = price_tag.find(p_css_sel, id=p_css_sel_name).text.strip()
            elif p_css_sel_attr == 'itemprop':
                price = price_tag.find(p_css_sel, itemprop=p_css_sel_name).text.strip()

            soup = BeautifulSoup(content, 'lxml')
            if nt_css_sel_attr == 'class':
                name_tag = soup.find(nt_css_sel, class_=nt_css_sel_name)
            elif nt_css_sel_attr == 'id':
                name_tag = soup.find(nt_css_sel, id=nt_css_sel_name)

            if n_css_sel_attr == 'class':
                name = name_tag.find(n_css_sel, class_=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'id':
                name = name_tag.find(n_css_sel, id=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'itemprop':
                name = name_tag.find(n_css_sel, itemprop=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'individual':
                name = soup.h1.text.strip()
        time.sleep(0.5)

        print(f"{shop} - successfully loaded")

    except AttributeError:
        print(f"{shop} - variable missing")
    except:
        print(f"{shop} - access denied")

    try:
        with sync_playwright() as p:  # playwright hinzugefügt
            browser = p.chromium.launch(executable_path=exe_path, headless=False, slow_mo=3000)
            page = browser.new_page()
            page.goto(url)
            page.screenshot(path=f"screenshot_{shop}_inco_{i}.png", full_page=True)
            content_inco = page.content()
            soup = BeautifulSoup(content_inco, 'lxml')
            if pt_css_sel_attr == 'class':
                inco_price_tag = soup.find(pt_css_sel, class_=pt_css_sel_name)
            elif pt_css_sel_attr == 'id':
                inco_price_tag = soup.find(pt_css_sel, id=pt_css_sel_name)
            if p_css_sel_attr == 'class':
                inco_price = inco_price_tag.find(p_css_sel, class_=p_css_sel_name).text.strip()
            elif p_css_sel_attr == 'id':
                inco_price = inco_price_tag.find(p_css_sel, id=p_css_sel_name).text.strip()
            elif p_css_sel_attr == 'itemprop':
                inco_price = inco_price_tag.find(p_css_sel, itemprop=p_css_sel_name).text.strip()
            ua = user_agent.replace(';', ',')
            row = pd.DataFrame({'url': [url], 'price': [price], 'inco_price': [inco_price], 'name': [name], 'ua': [ua],
                                'browser': [browser_version]})  # variablen in dataframe hinzufuegen
            df = pd.concat([df, row], ignore_index=True)
        time.sleep(0.5)

        print(f"{shop} - inco successfully loaded")

    except AttributeError:
        print(f"{shop} - inco variable missing")
    except:
        print(f"{shop} - inco access denied")

all_prices_df = pd.concat([all_prices_df, df], ignore_index=True)
all_prices_df.to_csv(user_profile + '\Desktop\prices_export.csv', index=False, header=True,
                     encoding='UTF-8')  # finalen dataframe in csv exportieren