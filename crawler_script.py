from bs4 import BeautifulSoup
import time
import pandas as pd
import os
from playwright.sync_api import sync_playwright

def path_def():
    p= ''
    for r,d,f in os.walk("C:\\"):
        for files in f:
            if files == "chrome.exe":
                p = os.path.join(r,files)
        if p != '':
            break
    return p

with sync_playwright() as s:
  browser = s.chromium.launch(headless = False, slow_mo =200)
  page = browser.new_page()
  page.goto('http://wieistmeinuseragent.de/')
  ua_content = page.content()
  soup = BeautifulSoup(ua_content, 'lxml')
  user_agent = soup.find('p', class_ = 'useragent').text.strip()

exe_path = path_def()
user_profile = os.environ['USERPROFILE']
data_dir= os.path.join(r'C:\Users', user_profile, r'AppData\Local\Google\Chrome\User Data')

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
    price = 0
    inco_price = 0

    try:

        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(executable_path = exe_path, user_data_dir= data_dir, headless=True, slow_mo=2500, user_agent=user_agent) 
            page = browser.new_page()
            page.goto(url)
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
                name_tmp = str(name_tag.find_all('h1'))
                name = soup.h1.text.strip()
        time.sleep(0.5)

        print(f"{shop} - successfully loaded")
    
    except AttributeError:
        print(f"{shop} - variable missing")
    except:
        print(f"{shop} - access denied")

    try:
        with sync_playwright() as p:    #playwright hinzugefügt
            browser = p.chromium.launch(headless=True, slow_mo=2500)
            page = browser.new_page()
            page.goto(url)
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
            row = pd.DataFrame({'url': [url], 'price': [price], 'inco_price': [inco_price],'name': [name]})  # variablen in dataframe hinzufuegen
            df = pd.concat([df, row], ignore_index=True)
        time.sleep(0.5)

        print(f"{shop} - inco successfully loaded")

    except AttributeError:
        print(f"{shop} - inco variable missing")
    except:
        print(f"{shop} - inco access denied")

all_prices_df = pd.concat([all_prices_df, df], ignore_index=True)
all_prices_df.to_csv(user_profile + '\Desktop\prices_export.csv', index = False, header = True, encoding = 'UTF-8') #finalen dataframe in csv exportieren