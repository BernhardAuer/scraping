from itemadapter import ItemAdapter
from parliament_speaker.items import SpeakerItem
import sys
import keyword
import re
from itemadapter import ItemAdapter

mappingDict = {
        "Nr.": "Nr",
        "Rede beendet": "HasSpeechFinishedRaw",
        "Redner/-innen": "NameOfSpeaker",
        "Anz. WM": "SpeechNumberOfTopicByAuthorRaw",
        "Art der Wortmeldung WM": "TypeOfSpeech",
        "Start": "Start",
        "Dauer": "LengthOfSpeech",
        "Limit": "TimeLimit"
    }
    
def mapDictKeys(dict):
    result = {}
    for key in dict.keys():
        if key in mappingDict:
            newKey = mappingDict[key] 
            result[newKey] = dict[key]
        else:
            # try to automap keys...
            cleanKeyName = clean(key)
            if keyword.iskeyword(cleanKeyName) is True:
                print("skipping field because variable name is a python keyword, could not transform dict to scrapy item!")
            else:
                result["autoGenerated_" + cleanKeyName] = dict[key]   
    result = SpeakerItem(**result)
    return result

# https://stackoverflow.com/questions/3303312/how-do-i-convert-a-string-to-a-valid-variable-name-in-python
def clean(s):
    # Remove invalid characters
    s = re.sub('[^0-9a-zA-Z_]', '', s)
    # Remove leading characters until we find a letter or underscore
    s = re.sub('^[^a-zA-Z_]+', '', s)
    return s

