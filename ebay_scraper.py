from ebaysdk.finding import Connection
import json, sys
from datetime import datetime
import math

def ebay_scraper(data):
    grandlist = list()

    api = Connection(config_file='myebay.yaml', debug=False, siteid="EBAY-US")

    for spot in range(len(data)):
        title = data[spot]['name']
        if '&' in title:
            title = title.replace('&', 'and')
        request = {
            'keywords' : title,
            'itemFilter' : [{'name' : 'FreeShippingOnly', 'value' : 'True'},{'name': 'Condition', 'value': 'New'}],
            'paginationInput': { 'entriesPerPage': 10 }
        }
        #Define list to save name, price and url
        itemlist = list()

        try:
            response = api.execute('findItemsByKeywords', request)
            for item in response.reply.searchResult.item:
                itemlist.append(dict(name=item.title, price=item.sellingStatus.currentPrice.value, link=item.viewItemURL))
        #Catch Possible Errors, Attribute happens when there are no responses, Connection happens when name raises error
        except AttributeError:
            print(f"{title} caused the error {sys.exc_info()[0]}")
        except ConnectionError:
            print(f"{title} causes the error {sys.exc_info()[0]}")
        #Creates list of each item
        grandlist.append(dict(name=title, items=itemlist))

    #List to combine both the GC Surplus data and the Ebay Results
    combinedlist = list()
    #Makes list into nice a readable format
    for spot in range(len(data)):
        combinedlist.append(dict(dict(gc=data[spot], ebay=grandlist[spot])))

    meanlist = list()
    for i in range(len(combinedlist)):
        count = 0
        if combinedlist[i]['ebay']['items']: #checks that the ebay api had results for the search
            for t in combinedlist[i]['ebay']['items']:
                #adds up price from each item in the product list
                count += float(t['price'])
        #Create dictionary with name, gcprice, mean ebay price, link to gc, and first link of ebay list
            meanlist.append(dict(name=combinedlist[i]['ebay']['name'],
                                 gcsurplusprice=combinedlist[i]['gc']['price'],
                                 meanpriceebay=math.floor(count/len(combinedlist[i]['ebay']['items'])),
                                 gclink=combinedlist[i]['gc']['link'],
                                 ebaylink=combinedlist[i]['ebay']['items'][0]['link']))
        else:
            #no results for ebay --> only show gc price, ebay price of 0 and gc link
            meanlist.append(dict(name=combinedlist[i]['ebay']['name'],
                                 gcsurplusprice=combinedlist[i]['gc']['price'],
                                 meanpriceebay=0,
                                 gclink=combinedlist[i]['gc']['link']))

    #Returns list of mean values for each product in pretty json format
    return json.dumps(meanlist,indent=4)