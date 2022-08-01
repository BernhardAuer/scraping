# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from pydantic import validate_arguments
import scrapy

@validate_arguments
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

