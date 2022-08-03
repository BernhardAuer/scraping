import scrapy
import re


class ParliamentarySessionsSpider(scrapy.Spider):
    name = "parliamentarySessions"
    start_urls = [
        'https://www.parlament.gv.at/PAKT/PLENAR/filter.psp?view=RSS&jsMode=&xdocumentUri=&filterJq=&view=&MODUS=PLENAR&NRBRBV=NR&GP=XXVII&R_SISTEI=SI&listeId=1070&FBEZ=FP_007',
    ]
   
    def parse(self, response):
        for quote in response.css('item'):
            yield {
                'title': quote.css('title::text').get().strip(),
                'pubDate': quote.css('pubDate::text').get().strip(),
                'link': quote.css('link::text').get().strip(),
            }

    
