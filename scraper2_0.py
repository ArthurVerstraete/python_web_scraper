from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from prettytable import PrettyTable as pt
import time
import datetime
now = datetime.datetime.now()

megekkoTable = pt(["Amount", "Name", "Unit Price", "Total Price"])
megekkoTotalTable = pt(["Total without shipping", "Shipping", "Total with shipping"])

bolTable = pt(["Amount", "Name", "Unit Price", "Total Price"])
bolTotalTable =  pt(["Total without shipping", "Shipping", "Total with shipping"])

maxICTTable = pt(["Amount", "Name", "Unit Price", "Total Price"])
maxICTTotalTable = pt(["Total without shipping", "Shipping", "Total with shipping"])

mediamarktTable = pt(["Amount", "Name", "Unit Price", "Total Price"])
mediamarktTotalTable = pt(["Total without shipping", "Shipping", "Total with shipping"])

totalTable = pt(["#products", "Total without shipping", "Total with shipping"])

megekkoTotalNShipping = 0
bolTotalNShipping = 0
maxICTTotalNShipping = 0
mediamarktTotalNShipping = 0
totalNShipping = 0
total = 0

megekkoShipping = 5.95
bolShipping = 0
maxICTShipping = 0
mediamarktShipping = 0

megekkoSites = ["https://www.megekko.nl/product/4278/261303/Socket-AM4-Processoren/AMD-Ryzen-5-3600-processor",
                "https://www.megekko.nl/product/4286/248686/AMD-Socket-AM4-Moederborden/Asrock-B450M-STEEL-LEGEND-moederbord",
                "https://www.megekko.nl/product/2046/185186/DDR4-Geheugen/G-Skill-DDR4-Aegis-2x8GB-3000Mhz-F4-3000C16D-16GISB-Geheugenmodule",
                "https://www.megekko.nl/product/1963/1093873/Nvidia-Videokaarten/Gigabyte-Geforce-GTX-1650-Super-OC-4G-Videokaart",
                "https://www.megekko.nl/product/4186/264373/PC-Voedingen-PSU-/Seasonic-Core-Gold-GC-650-PSU-PC-voeding",
                "https://www.megekko.nl/product/5093/266800/SSD-M-2/Kingston-A2000-1000GB-M-2-SSD",
                "https://www.megekko.nl/product/3419/1099052/Antistatische-producten/Nedis-Antistatische-Polsband-Verstelbaar-Zwart",
                "https://www.megekko.nl/product/2036/993706/Hard-disks-3-5-/Seagate-HDD-3-5-1TB-ST1000DM010-BarraCuda",
                "https://www.megekko.nl/product/1942/1085311/Wi-Fi-PCI-E-kaart/TP-LINK-WLAN-Adapter-Archer-TX3000",
                "https://www.megekko.nl/product/1995/376135/Case-fan-120mm/Gelid-Solutions-Casefan-SILENT-12-PWM-120mm",
                "https://www.megekko.nl/product/2060/259480/Laptop-Koeling/Ewent-EW1258-notebook-cooling-pad-43-2-cm-17-1000-RPM-Zwart",
                "https://www.megekko.nl/product/2177/102600/PC-speakers/Logitech-speakers-Z150-black"]

megekkoAmounts = [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1]

bolSites = ["https://www.bol.com/nl/p/gxt-165-celox-rgb-gaming-muis-10-000-dpi/9200000103300934/?bltgh=sXdumu3ch1pw9PNm8BdAMg.1_4.5.ProductTitle",
            "https://www.bol.com/nl/p/philips-243v7qdsb-full-hd-ips-monitor/9200000077546745/?bltgh=kD76BucF5X-IQdlwfyxCzw.1_4.5.ProductTitle"]

bolAmounts = [1 , 1]

maxICTSites = ["https://maxict.nl/hp-p27h-g4-686-cm-27-1920-x-1080-pixels-full-hd-ips-p15258407.html"]

maxICTAmounts = [1]

mediamarktSites = ["https://www.mediamarkt.be/nl/product/_trust-gamingtoetsenbord-azerty-22592-1718102.html?ga_query=22592"]

mediamarktAmounts = [1]

for x in range(len(megekkoSites)):
    uClient = uReq(megekkoSites[x])
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    title = page_soup.find("h1", {"class":"title"}).text
    euro = page_soup.find("div", {"class":"euro large"}).text.replace(',', '.')

    if euro.endswith('-'):
        price = round(float(euro.replace('-', '0')), 2)
    else:
        cents = page_soup.find("div", {"class":"cent large"}).text
        price = round(float(euro + cents), 2)

    megekkoTable.add_row([megekkoAmounts[x], title, "€ " + str(price), "€ " + str(megekkoAmounts[x]*price)])
    megekkoTotalNShipping = megekkoTotalNShipping + (megekkoAmounts[x]*price)

print("#MEGEKKO#")
print(megekkoTable)
megekkoTotalTable.add_row([megekkoTotalNShipping, megekkoShipping, round(megekkoTotalNShipping+megekkoShipping, 2)])
print(megekkoTotalTable)
totalNShipping = totalNShipping + megekkoTotalNShipping
total = total + (round(megekkoTotalNShipping+megekkoShipping, 2))
print('\n\n\n')

f = open(str("2.0_" + now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write("#MEGEKKO#")
f.write('\n')
f.write(str(megekkoTable))
f.write('\n')
f.write(str(megekkoTotalTable))
f.write('\n\n\n')

for x in range(len(bolSites)):
    uClient = uReq(bolSites[x])
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    title = page_soup.find("h1", {"class":"page-heading"}).text.replace('\n', '')
    priceDiv = page_soup.find("div", {"class": "price-block__price"})
    euro = priceDiv.find("span", {"data-test": "price"}).text.split('\n')[0]
    cents = priceDiv.find("sup", {"data-test": "price-fraction"}).text.replace('-', '0')
    price = round(float(euro + "." + cents), 2)
    bolTable.add_row([bolAmounts[x], title, "€ " + str(price), "€ " + str(bolAmounts[x]*price)])
    bolTotalNShipping = bolTotalNShipping + (bolAmounts[x]*price)

print("#BOL#")
print(bolTable)
bolTotalTable.add_row([bolTotalNShipping, bolShipping, round(bolTotalNShipping+bolShipping, 2)])
print(bolTotalTable)
totalNShipping = totalNShipping + bolTotalNShipping
total = total + (round(bolTotalNShipping+bolShipping, 2))
print('\n\n\n')

f = open(str("2.0_" + now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write("#BOL#")
f.write('\n')
f.write(str(bolTable))
f.write('\n')
f.write(str(bolTotalTable))
f.write('\n\n\n')

for x in range(len(maxICTSites)):
    uClient = uReq(maxICTSites[x])
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    title = page_soup.find("h1", {"class": "title-a"}).text
    priceDiv = page_soup.find("div", {"class": "swap-vat swap-price"})
    price = round(float(priceDiv.find("span", {"class": "pricing-value"}).text.replace(' ', '').replace(',', '.').replace('€', '')), 2)
    maxICTTable.add_row([maxICTAmounts[x], title, "€ " + str(price), "€ " + str(maxICTAmounts[x]*price)])
    maxICTTotalNShipping = maxICTTotalNShipping + (maxICTAmounts[x]*price)

print("#MAX ICT#")
print(maxICTTable)
maxICTTotalTable.add_row([maxICTTotalNShipping, maxICTShipping, round(maxICTTotalNShipping+maxICTShipping, 2)])
print(maxICTTotalTable)
totalNShipping = totalNShipping + maxICTTotalNShipping
total = total + (round(maxICTTotalNShipping+maxICTShipping, 2))
print('\n\n\n')

f = open(str("2.0_" + now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write("#MAX ICT#")
f.write('\n')
f.write(str(maxICTTable))
f.write('\n')
f.write(str(maxICTTotalTable))
f.write('\n\n\n')

for x in range(len(mediamarktSites)):
    uClient = uReq(mediamarktSites[x])
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    title = page_soup.find("h1", {"itemprop": "name"}).text
    price = round(float(page_soup.find("meta", {"itemprop": "price"})["content"]), 2)
    mediamarktTable.add_row([mediamarktAmounts[x], title, "€ " + str(price), "€ " + str(mediamarktAmounts[x]*price)])
    mediamarktTotalNShipping = mediamarktTotalNShipping + (mediamarktAmounts[x]*price)

print("#MEDIAMARKT#")
print(mediamarktTable)
mediamarktTotalTable.add_row([mediamarktTotalNShipping, mediamarktShipping, round(mediamarktTotalNShipping+mediamarktShipping, 2)])
print(mediamarktTotalTable)
totalNShipping = totalNShipping + mediamarktTotalNShipping
total = total + (round(mediamarktTotalNShipping+mediamarktShipping, 2))
print('\n\n\n')

f = open(str("2.0_" + now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write("#MEDIAMARKT#")
f.write('\n')
f.write(str(mediamarktTable))
f.write('\n')
f.write(str(mediamarktTotalTable))
f.write('\n\n\n')

print("#TOTAL#")
totalTable.add_row([len(megekkoSites)+len(bolSites)+len(maxICTSites)+len(mediamarktSites), totalNShipping, total])
print(totalTable)

f = open(str("2.0_" + now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write("#TOTAL#")
f.write('\n')
f.write(str(totalTable))