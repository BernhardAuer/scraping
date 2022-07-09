import scrapy
import re

class Helper():
    def parse():
        print("Das ist ein Test")

class QuotesSpider(scrapy.Spider):
    name = "topics"
    start_urls = [
        'https://www.parlament.gv.at/PAKT/VHG/XXVII/NRSITZ/NRSITZ_00165/index.shtml',
    ]
    custom_settings = {
    "FEED_EXPORT_ENCODING": "utf-8"
    }
   
    def parse(self, response):
        # some consts
        regularTop = 'TOP'.casefold()
        shortTop = 'Kurze Debatte'.casefold()


        # stripAll = lambda a : a.strip()
        for block in response.css('div.reiterBlock'):
            # captions = []
            captions = block.css('h3::text').getall()
            test = 'nix'
            for str in captions:
                if str.casefold().startswith(regularTop):
                    tables = block.css("table") #[3].css("tr td span::text,a::text").getall()

                    for table in tables:
                        content = table.css("tr td span::text,a::text").getall()
                        dict = {}
                    # for i in test.range() / 2:
                    #     dict[test[i*2]] = test[i*2+1]
                    #dict['hallo'] = 1
                    # dict[test[0]] = test[1]
                        yield {
                            # 'test': block.css('h3::text').getall(),
                            'test': content
                        }
            # if (caption is not None and caption.casefold.startswith(regularTop)):                
            #     test = 'test'#block.css('table')[2].css('tr td').get().strip()
            # yield {
            #     # 'test': block.css('h3::text').getall(),
            #     'test': test
            # }
            

    
