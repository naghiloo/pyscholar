import time
import json
import logging
from scholarly import scholarly
# from scholarly import Tor_Internal
from decouple import config, Csv

from functions import send_sms

log = logging.getLogger(__name__)

# pg = Tor_Internal()
# scholarly.use_proxy(pg)

def getScholar(author_id):
    log.info("getScholar | scraping author scholar informations")
    author = scholarly.search_author_id(author_id)
    log.info('getScholar | adding author basic, indices and publications information')
    scholarly.fill(author, sections=['basics', 'indices', 'publications'])

    return json.dumps(author, indent=2)

def cleanScholar(author_id):
    log.info('cleanScholar | removing some keys')
    result = json.loads(getScholar(author_id))
    result.pop('filled')
    result.pop('source')
    result.pop('email_domain')
    result.pop('organization')
    result.pop('interests')

    log.info('cleanScholar | calculating publications count')
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
    log.info('main | start')
    # TODO: create result.json file if does not exists
    log.info('main | reading saved information as json')
    r = open("result.json", "r")
    res = json.loads(r.read())

    res = {
        "publications": res["publications"],
        "citedby": res["citedby"],
        "hindex": res["hindex"]
    }

    log.info('main | loop over author_ids to get informations')
    for author_id in config('SCHOLAR_USERS', cast=Csv()):
        scholar = json.loads(cleanScholar(author_id))

    log.info('main | checking scholar changes with the local')
    if (res["citedby"] != scholar["citedby"]) or (res["hindex"] != scholar["hindex"]) or (res["publications"] != scholar["publications"]):
        log.info('main | there are some changes on the scholar')
        print(send_sms(scholar))

        log.info('main | opening result.json to save new changes. start to send a message')
        f = open("result.json", "w")
        f.write(json.dumps(scholar))
        f.close()
    
    r.close()
    
    log.info('main | sleep some moments')
    time.sleep(int(config('SLEEP_SECONDS')))