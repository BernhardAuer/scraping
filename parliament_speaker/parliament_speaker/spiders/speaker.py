from pickle import NONE
import scrapy
import re
from enum import Enum
from ..items import SpeakerItem
import sys
import pymongo
from parliament_speaker.spiders.SpeakerItemParser import mapDictKeys
from itemadapter import ItemAdapter

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
shortTopAbr = 'KD'
urgentRequest = 'Dringl' # dringl anfrage / dringliche anfrage / ...
hotTopic = 'Aktuelle Stunde:'
randomTopic = '"'
#speechTimeLimits = 'Blockredezeit'
#speechTimeLimitSingles = 'Redezeitbeschränkungen'

tableCaptionsStartChars = list(map(lambda x: x.casefold().strip(), [regularTop, urgentRequest, hotTopic, randomTopic, shortTopAbr, shortTop]))


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
    start_urls = []
    custom_settings = {
    "FEED_EXPORT_ENCODING": "utf-8"
    }

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def __init__(self, mongodb_uri, mongodb_db, *args, **kwargs):      
        super(QuotesSpider, self).__init__(*args, **kwargs) 
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        self.parliamentarySessions = list(self.db["parliamentarySessions"].find({}, {"_id":0,"Link":1, "Title":1, "Date":1})) # load into memory, cause this list is small
        # todo: close con
        self.start_urls = [session["Link"] for session in self.parliamentarySessions]     
          
        

   
    def parse(self, response):

        currentUrl = response.request.url
        currentParliamentarySession = list(filter(lambda x: x["Link"] == currentUrl, self.parliamentarySessions))[0] # single
        print(currentUrl)
        print(list(self.parliamentarySessions))
        block = response.css('div.reiterBlock')[3]

        captions = block.css('h3::text, h6 a::text').getall()
        filteredCaptions = list(filter(lambda cap: cap.casefold().strip().startswith(tuple(tableCaptionsStartChars)), captions))

        tables = block.css("table[summary='Rednerinnen und Redner der Debatte']")        
        i = 0
        for table in tables:   
            tableCaption = filteredCaptions[i] if i < len(filteredCaptions) else "unknown table"
            print("-----------------------------------------------------------------------------" + tableCaption)                 
            headerDict = self.getTableTextAsDict(table, TableType.tableHeader, None)
            resultDict = self.getTableTextAsDict(table, TableType.tableContent, (headerDict)[0])
            i += 1

            for item in resultDict:
                parsedSpeakerItem = mapDictKeys(item)
                parsedSpeakerItem.Topic = tableCaption
                parsedSpeakerItem.ParliamentarySessionTitle = currentParliamentarySession["Title"]
                yield parsedSpeakerItem
        

    def getTableTextAsDict(self, table, tableType, keyDict):
        parsedTable = Helper.parseTable(table, tableType)
        contentList = []
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
            contentList.append(content)
        return contentList
                            