# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field, InitVar
from datetime import date
from operator import truediv

@dataclass
class SpeakerItem:
   
    Nr: int
    HasSpeechFinished: bool = field(init=False)    
    SpeechNumberOfTopicByAuthor: int = field(init=False)
    NameOfSpeaker : str
    TypeOfSpeech : str
    Start: str
    TimeLimit: str
    LengthOfSpeech: str
    TypeOfSpeech: str
    ParliamentarySessionTitle: str = field(init=False)
    Topic: str = field(init=False)  
    SpeechNumberOfTopicByAuthorRaw: InitVar[str] = None
    HasSpeechFinishedRaw: InitVar[str] = None

    def __post_init__(self, SpeechNumberOfTopicByAuthorRaw, HasSpeechFinishedRaw): # order is relevant... OMG!!!!!!
        if HasSpeechFinishedRaw== '+':
            self.HasSpeechFinished = True
        else:
            self.HasSpeechFinished = False

        if SpeechNumberOfTopicByAuthorRaw == "":
            self.SpeechNumberOfTopicByAuthor = 1
        else:            
            self.SpeechNumberOfTopicByAuthor = int(SpeechNumberOfTopicByAuthorRaw)

        self.Nr = int(self.Nr)


        

