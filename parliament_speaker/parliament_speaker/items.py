# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field, InitVar
from datetime import date
from operator import truediv
from pydantic import validate_arguments

@dataclass
class SpeakerItem:
   
    Nr: int
    HasSpeakingFinished: bool = field(init=False)
    NameOfSpeaker : str
    TypeOfSpeak : str
    Start: str
    LimitOfSpeak: str
    LengthOfSpeak: str
    NumberOfSpeakes: str
    HasSpeakingFinishedRaw: InitVar[str]
    #TypeOfSpeakRaw: InitVar[str] = None
    def __post_init__(self, _HasSpeakingFinishedRaw):
        if _HasSpeakingFinishedRaw== '+':
            self.HasSpeakingFinished = True
        else:
            self.HasSpeakingFinished = False
