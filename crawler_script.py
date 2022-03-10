
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
from csv import writer
import time

prices = []
titles = []
prices_inco = []

#URLs einlesen aus csv
with open("import.csv") as file:

    # Öffnen mit Webbrowser

    for line in file:
        time.sleep(1)
        url = line

        #path kann weggelassen werden (nur zur sicherheit)
        path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s'
        webbrowser.get(path)
        webbrowser.open(url,new = 2)
        response = urllib.request.urlopen(url)
        content = response.read()

        #Preis extrahieren mit BeatifulSoup
        soup = BeautifulSoup(content,'lxml')

        #Preise in Lite speichern
        price_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")
        prices.append(price_tag)

        #Titel in Liste speichern
        title_tag = soup.find('div', class_ = "prd_module prd_module--noLine prd_shortInfo")
        titles.append(title_tag)

#URLs erneut einlesen aus csv
with open("import.csv") as file:

    for line in file:
        time.sleep(1)
        url = line
        path_inco = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s --incognito'
        webbrowser.get(path_inco).open(url,new= 2)
        response = urllib.request.urlopen(url)
        content = response.read()

        #Preis extrahieren mit BeatifulSoup
        soup = BeautifulSoup(content,'lxml')

        #Preise in Lite speichern
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


# Ziel Website
url = "https://www.otto.de/p/nike-sportswear-air-force-1-le-gs-sneaker-1229702164/#variationId=1229702854"



