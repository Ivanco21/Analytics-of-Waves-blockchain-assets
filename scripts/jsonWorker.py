# -*- coding: utf-8 -*-
import json

def jsonRead (jsonPth):
    try:
        with open(jsonPth, 'r', encoding = 'utf-8') as fh:
            information = json.load(fh)
            return information
    except (IOError, Exception) as e:
        print(e)
        
def getOneTag (json,tag):
    allTags= []
    for n in json:
        oneTag = n[tag]

        allTags.append(oneTag)
    return allTags

