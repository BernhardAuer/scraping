# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpeakerItem(scrapy.Item):
    

    Nr = scrapy.Field()
    HasSpeakingFinished = scrapy.Field()
    NameOfSpeaker = scrapy.Field()
    NumberOfSpeakes = scrapy.Field()
    TypeOfSpeak = scrapy.Field()
    Start = scrapy.Field()
    Dauer = scrapy.Field()

