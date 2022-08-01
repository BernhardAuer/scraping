# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy

@dataclass
class SpeakerItem:  

    Nr: int
    HasSpeakingFinished: str
    NameOfSpeaker : str
    NumberOfSpeakes: str
    TypeOfSpeak : str
    Start: str
    LimitOfSpeak: str
    LengthOfSpeak: str

