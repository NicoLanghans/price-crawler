#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
import re from bs4 \
import BeautifulSoup
import webbrowser
import urllib.request



# Allgemeine Einstellungen für Chrome (Selenium)
# PATH = "C:\Program Files (x86)\chromedriver.exe"
# ser = Service(PATH)
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(service=ser, options=options)

# Ziel Website
url = "https://www.otto.de/p/nike-sportswear-air-force-1-le-gs-sneaker-1229702164/#variationId=1229702854"

# Öffnen mit Selenium
#driver.get(url)

# Öffnen mit Webbrowser
webbrowser.open(url,new = 2)
response = urllib.request.urlopen(url)
content = response.read()

# content = webbrowser.open(url,new = 2)

#Preis extrahieren mit BeatifulSoup
soup = BeautifulSoup(content,'lxml')
price_tag = soup.find('div', class_ = "prd_price__main js_prd_price__main")
price = price_tag.find('span', id = "normalPriceAmount").text
print(price)

#push test