import re
from bs4 import BeautifulSoup
import webbrowser
import urllib.request
from csv import writer



# Ziel Website
url = "https://www.otto.de/p/nike-sportswear-air-force-1-le-gs-sneaker-1229702164/#variationId=1229702854"


# Öffnen mit Webbrowser
webbrowser.open(url,new = 2)
response = urllib.request.urlopen(url)
content = response.read()

#Preis extrahieren mit BeatifulSoup
soup = BeautifulSoup(content,'lxml')
price_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")

#Preis in csv schreiben
with open('shoe_prices.csv','w',newline='') as f:
    thewriter = writer(f)
    header = ['Price']
    thewriter.writerow(header)
    price = price_tag.find('span', id = "normalPriceAmount").text
    info = [price]
    thewriter.writerow(info)