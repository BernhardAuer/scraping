# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass, field, InitVar
from datetime import date, datetime
from operator import truediv
from pydantic import validate_arguments, ValidationError, validator
class Config:
    json_encoders = {
        datetime: lambda v: v.isoformat(),
    }

#@validate_arguments()
@dataclass
class ParliamentPlenarsitzungenItem():
    Title: str   
    Date: datetime = field(init=False)
    Link: str
    DateRaw: InitVar[str] = None
    def __post_init__(self, DateRaw):
        self.Date = datetime.strptime(
                DateRaw,
                "%d %b %Y %H:%M:%S %z"
            )
