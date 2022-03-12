from bs4 import BeautifulSoup
import webbrowser
import urllib.request
from csv import writer
import time
import keyboard
from winreg import *

prices = []
titles = []
prices_inco = []

# Erkennen des Default Browsers
def default_browser ():
    with OpenKey(HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice") as key:
        browser = QueryValueEx(key, 'Progid')[0]
    if browser == "ChromeHTML":
        return "chrome"
    if browser == "MSEdgeHTM":
        return "egde"
    if browser == "FirefoxURL-308046B0AF4A39CB":
        return "firefox"

def close_tab ():
    if default_browser() == "firefox":
        keyboard.press_and_release('Alt+F4')
    else:
        keyboard.press_and_release('ctrl+w')

#URLs einlesen aus csv - Untersuchter Preis
with open("import.csv") as file:
    
    for line in file:
        time.sleep(1)
        url = line

        #Öffnen mit Webbrowser
        path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        webbrowser.get(path)
        webbrowser.open(url,new = 1)
        response = urllib.request.urlopen(url)
        content = response.read()
        #Preis extrahieren mit BeatifulSoup
        soup = BeautifulSoup(content,'lxml')
        #Preise/Titel in Liste speichern
        price_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")
        prices.append(price_tag)
        title_tag = soup.find('div', class_ = "prd_module prd_module--noLine prd_shortInfo")
        titles.append(title_tag)
        #Browsertab schließen
        time.sleep(1)
        close_tab()

#URLs erneut einlesen aus csv - Vergleichspreis(Incognito)
with open("import.csv") as file:
    for line in file:
        time.sleep(1)
        url = line

        # Öffnen mit Webbrowser - Incognito
        path_inco = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s --incognito'
        webbrowser.get(path_inco).open(url,new= 2)
        response = urllib.request.urlopen(url)
        content = response.read()
        #Preis extrahieren mit BeatifulSoup
        soup = BeautifulSoup(content,'lxml')
        #Preise in Liste speichern
        price_inco_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")
        prices_inco.append(price_inco_tag)

#csv öffnen
#Preis in csv schreiben
with open('shoe_prices.csv','w',encoding= 'utf-8',newline='') as f:
        thewriter = writer(f)
        header = ['Price', 'Incognito Price', 'Title']
        thewriter.writerow(header)
        #kann man sicher schöner lösen
        for price_tag, title_tag, price_inco_tag in zip(prices, titles, prices_inco):
            price = price_tag.find('span', id = "normalPriceAmount").text
            title = title_tag.find('h1', class_ ="js_shortInfo__variationName prd_shortInfo__variationName").text
            inco = price_inco_tag.find('span', id = "normalPriceAmount").text
            info = [price, inco, title]
            thewriter.writerow(info)

