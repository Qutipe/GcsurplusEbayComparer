from ebaysdk.finding import Connection
import json, sys
from datetime import datetime

filename = f'gc-{datetime.today().strftime("%Y-%m-%d")}.json'
with open(filename, 'r') as f:
    data = json.load(f)

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

filename2 = f'gc-ebay-{datetime.today().strftime("%Y-%m-%d")}.json'
with open(filename2, 'w') as f:
    json.dump(combinedlist, f, indent=4)