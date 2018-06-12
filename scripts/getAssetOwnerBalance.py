# -*- coding: utf-8 -*-
import requests
import json

def jsonRead (jsonPth):
    try:
        with open(jsonPth, 'r', encoding = 'utf-8') as fh:
            information = json.load(fh)
            return information
    except (IOError, Exception) as e:
        print(e)

def getAssetassetId (information):
    allAssetsassetId = []
    for n in information:
        oneAssetId = n['assetid']
        oneOwner = n['issuer']
        tmp = []
        tmp.append(oneAssetId)
        tmp.append(oneOwner)
        allAssetsassetId.append(tmp)
    return allAssetsassetId

def setURLforRq(nodeName,listAssetAndOwner):
    allURL =[]
    for ids in listAssetAndOwner:
         # rest api : get /assets/balance/{address}/{assetId} 
        oneURL = 'http://' + nodeName + '/assets/balance/' + ids[1] +'/' + ids[0]
        allURL.append(oneURL)
    return allURL    


def main():
    #use public or main('127.0.0.1') waves node 
    node = 'nodes.wavesplatform.com'# public node
    
    information = jsonRead("parse_info\\assetsInfo.json")
    information.reverse()
    listAssetAndOwner = getAssetassetId(information)
    allURL = setURLforRq(node,listAssetAndOwner)
    ownerBalanses = []

    for url in allURL:
        try:
            rq = requests.get(url).json()
            ownerBalanses.append(rq)
            msg = "ok---" + url
            print(msg)
        except (ConnectionError, TimeoutError)as e:
                print(e)
    
    with open("parse_info\\ownerBalanses.json", mode='w', encoding='utf-8') as feedsjson:
        json.dump(ownerBalanses, feedsjson)    

if __name__ == "__main__":
        main()
