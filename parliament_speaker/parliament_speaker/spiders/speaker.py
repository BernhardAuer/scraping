import scrapy
import re

class Helper():
    def stripCharsFromList():
        return lambda a : a.strip()
        
    def parseTable(table):
        rows = table.css("tbody tr")       
        return rows

    def parseRow(row):
        cells = row.css("td")
        return cells
        
    def parseCells(cell):
        cellText = cell.css("span.table-responsive__inner::text, a::text").get()
        if cellText is None:
            cellText = cell.css("td.table-responsive__header::text").get()

        if cellText is not None:
            cellText = cellText.strip()
            cellText = cellText.replace("\u00A0", " ") # replace html non breaking spaces
        return cellText

    def parseTableHeader(table):
        headerRow = table.css("thead tr")
        return headerRow

    def parseHeaderRow(row):        
        cells = row.css("th")
        return cells

    def parseHeaderCells(cell):
        cellText = cell.css("::text").getall()
        cellText = " ".join(cellText)
        if cellText is not None:
            cellText = cellText.strip()
            cellText = cellText.replace("\u00A0", " ") # replace html non breaking spaces
        return cellText

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
                        headerDict = self.getTableHeaderAsDict(table)
                        parsedTable = Helper.parseTable(table)
                        for row in parsedTable:
                            parsedRow = Helper.parseRow(row)
                            i = 0
                            dict = {}
                            for cell in parsedRow:
                                parsedCell = Helper.parseCells(cell)
                                key = headerDict[i]
                                dict[key] = parsedCell
                                i = i + 1

                            yield dict

    def getTableHeaderAsDict(self, table):
        parsedTable = Helper.parseTableHeader(table)
        for row in parsedTable:
            parsedRow = Helper.parseHeaderRow(row)
            i = 0
            headerDict = {}
            for cell in parsedRow:
                parsedCell = Helper.parseHeaderCells(cell)
                headerDict[i] = parsedCell
                i = i + 1
        return headerDict
                            
            # if (caption is not None and caption.casefold.startswith(regularTop)):                
            #     test = 'test'#block.css('table')[2].css('tr td').get().strip()
            # yield {
            #     # 'test': block.css('h3::text').getall(),
            #     'test': test
            # }
            

    
