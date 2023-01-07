import time
import json
from scholarly import scholarly
# from scholarly import Tor_Internal
from decouple import config, Csv

from functions import send_sms

# pg = Tor_Internal()
# scholarly.use_proxy(pg)

def getScholar(author_id):
    author = scholarly.search_author_id(author_id)
    scholarly.fill(author, sections=['basics', 'indices', 'publications'])

    return json.dumps(author, indent=2)

def cleanScholar(author_id):
    result = json.loads(getScholar(author_id))
    result.pop('filled')
    result.pop('source')
    result.pop('email_domain')
    result.pop('organization')
    result.pop('interests')

    result['publications'] = len(result['publications'])

    # publications = {}

    # for item in result['publications']:
    #     # item = json.loads(item)

    #     item.pop('container_type')
    #     item.pop('source')
    #     item.pop('filled')
    #     item.pop('cites_id')

    #     publications.append(dict(item))
    
    # result['publications'] = json.dumps(publications)

    return json.dumps(result, indent=2)

while True:
    # TODO: create result.json file if does not exists
    r = open("result.json", "r")
    res = json.loads(r.read())

    res = {
        "publications": res["publications"],
        "citedby": res["citedby"],
        "hindex": res["hindex"]
    }

    for author_id in config('SCHOLAR_USERS', cast=Csv()):
        scholar = json.loads(cleanScholar(author_id))

    
    if (res["citedby"] != scholar["citedby"]) or (res["hindex"] != scholar["hindex"]) or (res["publications"] != scholar["publications"]):
        print(send_sms(scholar))
        f = open("result.json", "w")
        f.write(json.dumps(scholar))
        f.close()
    
    r.close()
    
    time.sleep(int(config('SLEEP_SECONDS')))