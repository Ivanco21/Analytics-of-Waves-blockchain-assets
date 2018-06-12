# -*- coding: utf-8 -*-
import requests
import json
import math
import time
import threading

# use public or main('127.0.0.1') waves node 
node = 'nodes.wavesplatform.com'# public node
nthreads = 10
block_with_first_asset = 236967

def blocks_reader(seq_from, seq_to, index):
    response = requests.get('http://%s/blocks/seq/%d/%d' % (node, seq_from, seq_to))
    if response.status_code == '200':
        try:
            thread_blocks[index] = response.json()
            return thread_blocks[index]
        except json.decoder.JSONDecodeError :
           print('JSONDecodeError')
    else:
        print(response.status_code)



last = requests.get('https://' + node + '/blocks/height').json()['height']
assetsID = []
for n in range(int(math.ceil((last - block_with_first_asset) / (nthreads * 100)) + 1)):
    thread_blocks = []
    thread = []
    for t in range(nthreads):
        thread_blocks.append('')
        thread.append(threading.Thread(target=blocks_reader, args=(
            max(1, last - (n + 1) * (nthreads * 100) + t * 100 + 1),
            last - n * (nthreads * 100) - ((nthreads * 100) - 100) + t * 100, t)))
        thread[t].start()
    blocks = []
    for t in range(nthreads):
        thread[t].join()
        if(thread_blocks[t] == list):
            blocks = blocks + thread_blocks[t]              
    for block in reversed(blocks):
        txs = block['transactions']
        for tx in reversed(txs):
            #type 'three' - it is a creation asset transaction ( four type - for transfer Waves and assets)
            if tx['type'] == 3:
                issue_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(tx['timestamp']/1000.))
                issuer = tx['sender']
                name = tx['name']
                assetid = tx['assetId']
                qt = tx['quantity']
                dec = tx['decimals']
                reissuable = tx['reissuable']
                des = tx['description'].replace('\n',' ')
                asset_data = {
                     'issue_time': issue_time,
                     'issuer': issuer,
                     'name':name, 
                     'assetid': assetid,
                     'qt' : qt,
                     'dec' : dec,
                     'reissuable':reissuable,
                     'description' : des
                }
                assetsID.append(asset_data)
                print(len(assetsID))
                
with open('parse_info\\assetsInfo.json', mode='w', encoding='utf-8') as feedsjson:
    json.dump(assetsID, feedsjson)
