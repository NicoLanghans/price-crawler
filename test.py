import keyboard
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
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

df = pd.DataFrame( columns = ["url", "price"])
all_prices_df = pd.DataFrame( columns = ["url", "price"])
df_input = pd.read_csv('import_url.csv')
i = 0
for row in df_input.itertuples():
    url = row[1]
    pt_css_sel = row[2]
    pt_css_sel_attr = row[3]
    pt_css_sel_name = row[4]
    p_css_sel = row[5]
    p_css_sel_attr = row[6]
    p_css_sel_name = row[7]

    webbrowser.open(url,new = 1)
    response = urllib.request.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content,'lxml')
    if pt_css_sel_attr == 'class_':
        price_tag = soup.find(pt_css_sel, class_ = pt_css_sel_name)
    elif pt_css_sel_attr == 'id':
        price_tag = soup.find(pt_css_sel, id = pt_css_sel_name)
    
    if p_css_sel_attr == 'class_':
        price = price_tag.find(p_css_sel, class_ = p_css_sel_name).text.strip()
    elif p_css_sel_attr == 'id':
        price = price_tag.find(p_css_sel, id = p_css_sel_name).text.strip()
    
    row = pd.DataFrame({'url': [url], 'price': [price]})
    df = pd.concat([df,row], ignore_index = True)
    close_tab()
all_prices_df = pd.concat([all_prices_df, df], ignore_index = True)
all_prices_df.to_csv(r'C:\Users\nico-\Documents\Fh Wedel Master\Seminar Personalisierte Preise\prices_export.csv', index = False, Header = True)











