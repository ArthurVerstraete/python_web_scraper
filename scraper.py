from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from prettytable import PrettyTable as pt
import time
import datetime
now = datetime.datetime.now()

my_url = 'https://tweakers.net/gallery/1204824/wenslijst/'

# opening up connection, grabbing the page 
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, 'html.parser')

inventoryBlock = page_soup.find("div", {"class":"inventory"})
inventoryId = inventoryBlock["id"]
tableDivClass = inventoryId + "_info"
tableDiv = page_soup.find("div", {"id":tableDivClass})
tableBody = tableDiv.table.tbody
tableRows = tableBody.findAll("tr", {})

outputTable = pt()
outputTable.field_names = ["Title", "Cheapest Shop", "Price #1", "Second Cheapest Shop", "Price #2", "Third Cheapest Shop", "Price #3"]

outputTable2 = pt()
outputTable2.field_names = ["#products", "Total", "Total According To Tweakers", "Difference", "Procentual Difference"]

total = 0
i = 0

for tableRow in tableRows:
    numberOfRows = len(tableRows)
    if (i == (numberOfRows - 1)):
        priceAccordingToTweakers = tableRow.find("td", {"class":"price"}).text
        priceAccordingToTweakers = priceAccordingToTweakers.replace('€', '').replace('.', '').replace(',', '.').replace('-', '0').replace(' ', '')
        priceAccordingToTweakers = round(float(priceAccordingToTweakers), 2)
        break
    tableRowUrl = tableRow.find("p", {"class":"ellipsis"}).a["href"]
    print("Scraping " + tableRowUrl)
    uItemClient = uReq(tableRowUrl)
    item_html = uItemClient.read()
    uItemClient.close()
    item_soup = soup(item_html, 'html.parser')
    title = item_soup.find("a", {"href":tableRowUrl}).text
    shopTable = item_soup.findAll(lambda tag: tag.name == 'table' and tag.get('class') == ['shop-listing'])
    shopTableRows = shopTable[0].findAll("tr", {})
    cheapestShopsName = ["", "", ""]
    cheapestShopsPrice = ["", "", ""]
    if int(len(shopTableRows)/6) >= 3:
        u = 13
        s = 6
    elif int(len(shopTableRows)/6) == 2:
        u = 7
        s = 6
    else:
        u = 1
        s = 1

    for x in range(0, u, s):
        cheapestShop = shopTableRows[x]
        cheapestShopsName[int(x/6)] = cheapestShop.find("td", {"class":"shop-name"}).p.a.text.replace('\n', '')
        cheapestShopsPrice[int(x/6)] = cheapestShop.find("td", {"class":"shop-price"}).p.a.text.replace('\n', '')
    outputTable.add_row([title, cheapestShopsName[0], cheapestShopsPrice[0], cheapestShopsName[1], cheapestShopsPrice[1], cheapestShopsName[2], cheapestShopsPrice[2]])
    price = cheapestShopsPrice[0].replace(' ', '').replace('€', '').replace('-', '0').replace(',', '.')
    total = total + float(price)
    i = i + 1
    time.sleep(20)

print(outputTable)
outputTable2.add_row([len(tableRows)-1, "€ " + str(round(total, 2)), "€ " + str(priceAccordingToTweakers), "€ " + str(round(total-priceAccordingToTweakers, 2)), str(round((((total-priceAccordingToTweakers)/priceAccordingToTweakers)*100), 4)) + " %"])
print(outputTable2)
f = open(str(now.strftime("%d-%m-%Y_%H:%M:%S")).replace(':', '') + ".txt", 'a')
f.write(str(outputTable))
f.write("\n" + str(outputTable2))