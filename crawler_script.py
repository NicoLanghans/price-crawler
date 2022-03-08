from bs4 import BeautifulSoup
import webbrowser
import urllib.request
from csv import writer
import time


# Ziel Website
#urls = ["https://www.otto.de/p/nike-sportswear-air-force-1-le-gs-sneaker-1229702164/#variationId=1229702854", "https://www.otto.de/p/nike-sportswear-court-vision-low-sneaker-860786554/#variationId=860787754", "https://www.otto.de/p/ashley-brooke-by-heine-hosenanzug-1324918231/#variationId=1324918243"]

#Listen und Laufvariable definieren

prices = []
titles = []

#URLs einlesen aus csv
with open("import.csv") as file:

    # Öffnen mit Webbrowser
    # Test mit einfacher Schleife
    # kann man vlt lieber mit einer for schleife bauen?

    for line in file:
        time.sleep(1)
        url = line
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



#csv öffnen
#Preis in csv schreiben

with open('shoe_prices.csv','w',encoding= 'utf-8',newline='') as f:
        thewriter = writer(f)
        header = ['Price', 'Title']
        thewriter.writerow(header)

        for price_tag, title_tag in zip(prices, titles):
            price = price_tag.find('span', id = "normalPriceAmount").text
            title = title_tag.find('h1', class_ ="js_shortInfo__variationName prd_shortInfo__variationName").text
            info = [price, title]
            thewriter.writerow(info)
