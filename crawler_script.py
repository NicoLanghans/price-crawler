import keyboard
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import time
from winreg import *
import pandas as pd
import os
import pathlib
from playwright.sync_api import sync_playwright


def default_browser():
    with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
        browser = QueryValueEx(key, 'Progid')[0]
    if browser == "ChromeHTML":
        return "chrome.exe"
    if browser == "MSEdgeHTM":
        return "msedge.exe"
    if browser == "FirefoxURL-308046B0AF4A39CB":
        return "Firefox"


def close_tab():
    if default_browser() == "Firefox":
        keyboard.press_and_release('Alt+F4')
    else:
        keyboard.press_and_release('ctrl+w')

def path_def():
    def find_path():
        p= ''
        for r,d,f in os.walk("C:\\"):
            for files in f:
                if files == "chrome.exe":
                    p = os.path.join(r,files)
            if p != '':
                break
        return p

    p = find_path() + ' %s'
    path_tmp = pathlib.PureWindowsPath(p)
    path = path_tmp.as_posix()
    return path

path = path_def()

#user_agent = open('user_agent.txt','r').readline().strip() #user agent aus Textdatei auf Variable zuweisen
#headers = {'User-Agent': user_agent}

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

        #webbrowser.get(path).open(url, new=1)  # browsertab oeffnen und Informationen abfragen
        #request = urllib.request.Request(url, None, headers)  # Anfrage mit header/ user agent
        #response = urllib.request.urlopen(request, timeout=5)   #timeout hinzugefügt
        #content = response.read()
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=r'C:\Users\Marc\AppData\Local\Google\Chrome\User Data', headless=False, slow_mo=1000,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36')
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

        print(price_tag)

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

        print(name_tag)
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
        close_tab()
        print(f"{shop} - successfully loaded")

        #path_inco = path + ' --incognito'  #informationen incognito abfragen
        #webbrowser.get(path_inco).open(url, new=2)
        #request = urllib.request.Request(url, None, headers)  # Anfrage mit header
        #response = urllib.request.urlopen(request, timeout=5)
        #content = response.read()

        with sync_playwright() as p:    #playwright hinzugefügt
            browser = p.chromium.launch(headless=False, slow_mo=1000)
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
        close_tab()
        
    except AttributeError:
        close_tab()
        print(f"{shop} - variable missing")
    except:
        close_tab()
        print(f"{shop} - access denied")

    time.sleep(1)

all_prices_df = pd.concat([all_prices_df, df], ignore_index=True)
user_profile = os.environ['USERPROFILE']
all_prices_df.to_csv(user_profile + '\Desktop\prices_export.csv', index = False, header = True, encoding = 'UTF-8') #finalen dataframe in csv exportieren