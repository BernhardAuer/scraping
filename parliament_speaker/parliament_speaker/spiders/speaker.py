import scrapy
import re
from enum import Enum
from ..items import SpeakerItem

class TableType(Enum):
    tableHeader = "table-header"
    tableContent = "table-content"

contentBlock = {    
    0 : "uebersicht",   
    1 : "sitzungsverlauf",
    2 : "beschluesse",
    3 : "rednerinnen",
    4 : "vorl_steno_protokoll"
}
# some consts
regularTop = 'TOP'
shortTop = 'Kurze Debatte'
urgentRequest = 'Dringl' # dringl anfrage / dringliche anfrage / ...
hotTopic = 'Aktuelle Stunde:'
randomTopic = '"'
#speechTimeLimits = 'Blockredezeit'
#speechTimeLimitSingles = 'Redezeitbeschränkungen'

tableCaptionsStartChars = list(map(lambda x: x.casefold().strip(), [regularTop, urgentRequest, hotTopic, randomTopic]))


cssSelectors = {
    TableType.tableHeader : { 
        "row" : "thead tr",
        "cell": "th",
        "cell-content": "::text",
     },
     TableType.tableContent : {
        "row" : "tbody tr",
        "cell": "td",
        "cell-content": "span.table-responsive__inner::text, a::text",
     }
}

class Helper():        
    def parseTable(table, tableType):
        rows = table.css(cssSelectors[tableType]["row"])       
        return rows

    def parseRow(row, tableType):
        cells = row.css(cssSelectors[tableType]["cell"])
        return cells
        
    def parseCells(cell, tableType):
        cellSelector = cell.css(cssSelectors[tableType]["cell-content"])

        if tableType == TableType.tableHeader:
            cellText = cellSelector.getall()
            cellText = " ".join(cellText)
        if tableType == TableType.tableContent:
            cellText = cellSelector.get()
            if cellText is None:
                cellText = cell.css("td.table-responsive__header::text").get() # alternative parsing for special tables...

        if cellText is not None:
            cellText = cellText.strip()
            cellText = cellText.replace("\u00A0", " ") # replace html non breaking spaces
        return cellText


class QuotesSpider(scrapy.Spider):
    name = "topics"
    start_urls = [
        'https://www.parlament.gv.at/PAKT/VHG/XXVII/NRSITZ/NRSITZ_00141/index.shtml',
    ]
    custom_settings = {
    "FEED_EXPORT_ENCODING": "utf-8"
    }
   
    def parse(self, response):
        block = response.css('div.reiterBlock')[3]

        captions = block.css('h3::text, h6 a::text').getall()
        filteredCaptions = list(filter(lambda cap: cap.casefold().strip().startswith(tuple(tableCaptionsStartChars)), captions))

        tables = block.css("table[summary='Rednerinnen und Redner der Debatte']")        
        i = 0
        for table in tables:   
            tableCaption = filteredCaptions[i] if i < len(filteredCaptions) else "unknown table"
            print("-----------------------------------------------------------------------------" + tableCaption)                 
            headerDict = self.getTableTextAsDict(table, TableType.tableHeader, None)
            resultDict = self.getTableTextAsDict(table, TableType.tableContent, list(headerDict)[0])
            i += 1
            yield from resultDict
        

    def getTableTextAsDict(self, table, tableType, keyDict):
        parsedTable = Helper.parseTable(table, tableType)
        for row in parsedTable:
            parsedRow = Helper.parseRow(row, tableType)
            i = 0
            content = {}
            for cell in parsedRow:
                parsedCell = Helper.parseCells(cell, tableType)

                if keyDict is not None:
                    key = keyDict[i]
                else:
                    key = i
                content[key] = parsedCell
                i += 1
            yield content
                            