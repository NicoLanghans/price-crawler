import keyboard
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
import time
from winreg import *
import pandas as pd

def default_browser ():
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

df = pd.DataFrame( columns = ["url", "price","inco_price", "name"]) #benoetigte dataframes initialisieren
all_prices_df = pd.DataFrame( columns = ["url", "price","inco_price", "name"])
df_input = pd.read_csv('import_url.csv')
i = 0
for row in df_input.itertuples():               #csv Input den Variablen zuweisen
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

    webbrowser.open(url,new = 1)              #browsertab oeffnen und Informationen abfragen
    response = urllib.request.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content,'lxml')
    if pt_css_sel_attr == 'class':
        price_tag = soup.find(pt_css_sel, class_ = pt_css_sel_name)
    elif pt_css_sel_attr == 'id':
        price_tag = soup.find(pt_css_sel, id = pt_css_sel_name)

    if p_css_sel_attr == 'class':
        price = price_tag.find(p_css_sel, class_ = p_css_sel_name).text.strip()
    elif p_css_sel_attr == 'id':
        price = price_tag.find(p_css_sel, id = p_css_sel_name).text.strip()
    
    if nt_css_sel_attr == 'class':
        name_tag = soup.find(nt_css_sel, class_ = nt_css_sel_name)
    elif nt_css_sel_attr == 'id':
        name_tag = soup.find(nt_css_sel, id = nt_css_sel_name)

    if n_css_sel_attr == 'class':
        name = name_tag.find(n_css_sel, class_ = n_css_sel_name).text.strip()
    elif n_css_sel_attr == 'id':
        name = name_tag.find(n_css_sel, id = n_css_sel_name).text.strip()
    elif n_css_sel_attr == 'content':
        name = name_tag.find(n_css_sel, content = n_css_sel_name).text.strip()
    close_tab()
    
    path_inco = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s --incognito'        #informationen incognito abfragen
    webbrowser.get(path_inco).open(url,new= 2)
    response = urllib.request.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content,'lxml')
    
    if pt_css_sel_attr == 'class':
        inco_price_tag = soup.find(pt_css_sel, class_ = pt_css_sel_name)
    elif pt_css_sel_attr == 'id':
        inco_price_tag = soup.find(pt_css_sel, id = pt_css_sel_name)
    
    if p_css_sel_attr == 'class':
        inco_price = inco_price_tag.find(p_css_sel, class_ = p_css_sel_name).text.strip()
    elif p_css_sel_attr == 'id':
        inco_price = inco_price_tag.find(p_css_sel, id = p_css_sel_name).text.strip()

    row = pd.DataFrame({'url': [url], 'price': [price], 'inco_price': [inco_price], 'name': [name]}) #variablen in dataframe hinzufuegen
    df = pd.concat([df,row], ignore_index = True)
    time.sleep(1)
    
all_prices_df = pd.concat([all_prices_df, df], ignore_index = True)
all_prices_df.to_csv(r'C:\Users\nico-\Documents\Fh Wedel Master\Seminar Personalisierte Preise\prices_export.csv', index = False, header = True, encoding = 'UTF-8') #finalen dataframe in csv exportieren

