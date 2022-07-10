# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import keyword
import re


class SpeakerItem(scrapy.Item):
    def __init__(self):
        scrapy.Item = self.mapDictKeys(scrapy.Item)

    Nr = scrapy.Field()
    RedeBeendet = scrapy.Field()
    RednerInnen = scrapy.Field()
    Nrt = scrapy.Field()

    def mapDictKeys(self, dict):
        result = {}
        for key in dict:
            cleanKeyName = self.clean(key)
            if keyword.iskeyword(cleanKeyName) is True:
                raise Exception("variable name is a python keyword, could not transform dict to scrapy item!")
            result[cleanKeyName] = dict[key]

        if len(dict) != len(result):
            raise Exception("error while mapping dict to scrapy item, probably because there are different keys in the original dict which will mapped to the same keys after transforming ...")
        return result

    # https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
    def clean(self, s):
        # Remove invalid characters
        s = re.sub('[^0-9a-zA-Z_]', '', s)

        # Remove leading characters until we find a letter or underscore
        s = re.sub('^[^a-zA-Z_]+', '', s)

        return s

