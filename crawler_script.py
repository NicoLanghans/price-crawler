from bs4 import BeautifulSoup
import webbrowser
import urllib.request
from csv import writer
import time


# Ziel Website
urls = ["https://www.otto.de/p/nike-sportswear-air-force-1-le-gs-sneaker-1229702164/#variationId=1229702854", "https://www.otto.de/p/nike-sportswear-court-vision-low-sneaker-860786554/#variationId=860787754", "https://www.otto.de/p/ashley-brooke-by-heine-hosenanzug-1324918231/#variationId=1324918243"]

i = 0
prices = []
titles = []


# Öffnen mit Webbrowser
# Test mit einfacher Schleife
# kann man vlt lieber mit einer for schleife bauen?
while i < len(urls):
    time.sleep(1)
    url = urls[i]
    webbrowser.open(url,new = 2)
    response = urllib.request.urlopen(url)
    content = response.read()

    #Preis extrahieren mit BeatifulSoup
    soup = BeautifulSoup(content,'lxml')
    price_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")
    prices.append(price_tag)

    #title_tag = soup.find('div', class_ = "js_shortInfo__variationName prd_shortInfo__variationName").text
    #titles.append(title_tag)
    #könnte man vlt ergänzen wenn es funktioniert

    i += 1

#Preis in csv schreiben
with open('shoe_prices.csv','w',newline='') as f:
        thewriter = writer(f)
        header = ['Price', 'Title']
        thewriter.writerow(header)

        for price_tag in prices:
            price = price_tag.find('span', id = "normalPriceAmount").text
            #title = titles
            info = [price]
            thewriter.writerow(info)