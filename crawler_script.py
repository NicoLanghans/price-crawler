from bs4 import BeautifulSoup
import time
from winreg import *
import pandas as pd
import os
from playwright.sync_api import sync_playwright


user_agent = open('user_agent.txt','r').readline().strip() #user agent aus Textdatei auf Variable zuweisen
user_profile = os.environ['USERPROFILE']
#data_dir = 'C:\Users\%s' + user_profile + '\AppData\Local\Google\Chrome\User Data'

df = pd.DataFrame(columns=["url", "price", "inco_price", "name"])  # benoetigte dataframes initialisieren
all_prices_df = pd.DataFrame(columns=["url", "price", "inco_price", "name"])
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

    try:

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(user_data_dir=r'C:\Users\nico-\AppData\Local\Google\Chrome\User Data', headless=True, slow_mo=2500,
            user_agent=user_agent) 
            page = browser.new_page()
            page.goto(url)
            p_content = page.inner_html(pt_css_sel) #selektor für preis eingefügt
            n_content = page.inner_html(nt_css_sel) #selektor für name eingefügt
            soup = BeautifulSoup(p_content, 'lxml')
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
            soup = BeautifulSoup(n_content, 'lxml')
            if nt_css_sel_attr == 'class':
                name_tag = soup.find(nt_css_sel, class_=nt_css_sel_name)
            elif nt_css_sel_attr == 'id':
                name_tag = soup.find(nt_css_sel, id=nt_css_sel_name)

            soup = BeautifulSoup(n_content, 'lxml')
            if n_css_sel_attr == 'class':
                name = name_tag.find(n_css_sel, class_=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'id':
                name = name_tag.find(n_css_sel, id=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'itemprop':
                name = name_tag.find(n_css_sel, itemprop=n_css_sel_name).text.strip()
            elif n_css_sel_attr == 'individual':
                name_tmp = str(name_tag.find_all('h1'))
                name = soup.h1.text.strip()
            time.sleep(0.5)
            browser.close()
        print(f"{shop} - successfully loaded")

        with sync_playwright() as p:    #playwright hinzugefügt
            browser = p.chromium.launch(headless=True, slow_mo=2500)
            page = browser.new_page()
            page.goto(url)
            content_inco = page.inner_html(pt_css_sel) #Variable content inco erstell und selektor eingefügt
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
            row = pd.DataFrame({'url': [url], 'price': [price], 'inco_price': [inco_price],'name': [name]})  # variablen in dataframe hinzufuegen
            df = pd.concat([df, row], ignore_index=True)
            time.sleep(0.5)
            browser.close()

    except AttributeError:
        print(f"{shop} - variable missing")
    except:
        print(f"{shop} - access denied")

    #time.sleep(1)

all_prices_df = pd.concat([all_prices_df, df], ignore_index=True)
all_prices_df.to_csv(user_profile + '\Desktop\prices_export.csv', index = False, header = True, encoding = 'UTF-8') #finalen dataframe in csv exportieren