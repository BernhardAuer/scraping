# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import sys
import keyword
import re

class TransformPipeline:
    mappingDict = {
        "Nr.": "Nr",
        "Rede beendet": "HasSpeakingFinished",
        "Redner/-innen": "NameOfSpeaker",
        "Anz. WM": "NumberOfSpeakes",
        "Art der Wortmeldung WM": "TypeOfSpeak",
        "Start": "Start",
        "Dauer": "LengthOfSpeak",
        "Limit": "LimitOfSpeak"
    }
    
    def mapDictKeys(self, dict):
        result = {}
        for key in dict.keys():
            if key in self.mappingDict:
                newKey = self.mappingDict[key] 
                result[newKey] = dict[key]
            else:
                # try to automap keys...
                cleanKeyName = self.clean(key)
                if keyword.iskeyword(cleanKeyName) is True:
                    print("skipping field because variable name is a python keyword, could not transform dict to scrapy item!")
                else:
                    result["autoGenerated_" + cleanKeyName] = dict[key]
            
        return result


    # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
    def clean(self, s):
        # Remove invalid characters
        s = re.sub('[^0-9a-zA-Z_]', '', s)

        # Remove leading characters until we find a letter or underscore
        s = re.sub('^[^a-zA-Z_]+', '', s)

        return s

    def process_item(self, item, spider):
        item = self.mapDictKeys(item)
        return item



class MongoDBPipeline:

    collection = 'scrapy_items'

    def __init__(self, mongodb_uri, mongodb_db):
        self.mongodb_uri = mongodb_uri
        self.mongodb_db = mongodb_db
        if not self.mongodb_uri: sys.exit("You need to provide a Connection String.")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongodb_uri=crawler.settings.get('MONGODB_URI'),
            mongodb_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.mongodb_db]
        # Start with a clean database
        self.db[self.collection].delete_many({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = (item) # needs to be a dict?
        self.db[self.collection].insert_one(data)
        return item