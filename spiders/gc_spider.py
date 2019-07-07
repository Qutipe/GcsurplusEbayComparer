import scrapy
import json
from datetime import datetime

'''
pip install pywin32
pip install ebaysdk
pip install scrapy

cd Gcsurplus_scraper\Gcsurplus_scraper

must create yaml file. 
example file is found in scrapyTutorial
'''
class GCSpider(scrapy.Spider):
    #name used when called in console
    name = "gc"

    def start_requests(self):
        urls = ["https://www.gcsurplus.ca/mn-eng.cfm?snc=wfsav&sc=ach-shop&jstp=sly&hpsr=&hpcs=5800&vndsld=0&rpp=25"] #Communication Stuff
        #urls=["https://www.gcsurplus.ca/mn-eng.cfm?snc=wfsav&sc=ach-shop&jstp=sly&hpsr=&hpcs=7000&vndsld=0&rpp=25"] #Computer stuff

        #Sends Request to get html from site
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # get names of all products
        names = response.css("tbody div.novisit a::text").getall()
        namelist = [str(name).strip() for name in names if str(name).strip()]

        # get minimum bid
        minbids = response.css("tbody dl.table-display dd.short::text").getall()
        bidlist = [str(bid).strip() for bid in minbids if str(bid).strip()]
        # need to match price with its heading to only take ones that are paired with minimum bid
        attrlist = response.css("tbody dl.table-display dt.short::text").getall()
        cleanedattr = [str(a).strip() for a in attrlist if str(a).strip()]

        # the prices
        grandlist = list(zip(cleanedattr, bidlist))
        pricelist = [y for x, y in grandlist if "minimum bid:" in x.lower()]

        # getting the links
        links = response.css("tbody div.novisit a::attr(href)").getall()
        linkslist = ["https://www.gcsurplus.ca/" + links[link] for link in range(len(links))]

        # store in dictionaries of three things
        finallist = list()
        for i in range(len(namelist)):
            finallist.append(dict(name=namelist[i], price=pricelist[i], link=linkslist[i]))

        #Saving File
        filename = f'gc-{datetime.today().strftime("%Y-%m-%d")}.json'
        with open(filename, 'w') as f:
            json.dump(finallist,f, indent=4)
        self.log(f'Saved file {filename}')
        self.log(f'Length of file {len(finallist)}')