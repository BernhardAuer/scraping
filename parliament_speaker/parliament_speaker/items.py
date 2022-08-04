# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field, InitVar
from datetime import date
from operator import truediv
import re

@dataclass
class SpeakerItem:
   
    Nr: int
    HasSpeechFinished: bool = field(init=False)    
    SpeechNumberOfTopicByAuthor: int = field(init=False)
    NameOfSpeaker : str
    TypeOfSpeech : str
    Start: str
    TimeLimit: str
    LengthOfSpeechRaw: InitVar[str] = None
    LengthOfSpeechInSec: int = field(init=False)
    TypeOfSpeech: str
    ParliamentarySessionTitle: str = field(init=False)
    Topic: str = field(init=False)  
    SpeechNumberOfTopicByAuthorRaw: InitVar[str] = None
    HasSpeechFinishedRaw: InitVar[str] = None

    def __post_init__(self, LengthOfSpeechRaw, SpeechNumberOfTopicByAuthorRaw, HasSpeechFinishedRaw): # order is relevant... OMG!!!!!!
        if LengthOfSpeechRaw != "":
            regexResult = re.search("(\d)*:(\d{2})", LengthOfSpeechRaw) 
            min = int(regexResult.group(1)) if regexResult.group(1) is not None else 0
            sec = int(regexResult.group(2)) if regexResult.group(2) is not None else 0
            self.LengthOfSpeechInSec = sec + (min * 60)

        if HasSpeechFinishedRaw== '+':
            self.HasSpeechFinished = True
        else:
            self.HasSpeechFinished = False

        if SpeechNumberOfTopicByAuthorRaw == "":
            self.SpeechNumberOfTopicByAuthor = 1
        else:            
            self.SpeechNumberOfTopicByAuthor = int(SpeechNumberOfTopicByAuthorRaw)

        self.Nr = int(self.Nr)


        

