import scrapy
import re

class Helper():
    def stripCharsFromList():
        return lambda a : a.strip()

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
                        
                        # there is a list full of key value pairs, so we need to transform these into a dict
                        dict = {}
                        for i in range((int( len(content) / 2))):                            
                            dict[content[i*2]] = content[(i*2)+1]
                        # content = list(map(lambda x: x.strip(), content))
                        
                    # for i in test.range() / 2:
                    #     dict[test[i*2]] = test[i*2+1]
                    #dict['hallo'] = 1
                    # dict[test[0]] = test[1]
                        yield {
                            # 'test': block.css('h3::text').getall(),
                            'test': dict
                        }
            # if (caption is not None and caption.casefold.startswith(regularTop)):                
            #     test = 'test'#block.css('table')[2].css('tr td').get().strip()
            # yield {
            #     # 'test': block.css('h3::text').getall(),
            #     'test': test
            # }
            

    
