import time
import json
import requests
from bs4 import BeautifulSoup
from decouple import config, Csv

from functions import send_sms


url = config('SCHOLAR_URL')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


while True:
    f = open("result.json", "r")
    res = json.loads(f.read())

    res = {
        "publications": res["publications"],
        "citedby": res["citedby"],
        "hindex": res["hindex"],
        "i10-index": ""
    }

    data = requests.get(url, headers=headers).text
    soup = BeautifulSoup(data, 'html.parser')
    citedby = soup.find(id='gsc_rsb_st')
    publications = soup.find(id='gsc_a_t')

    result = {
        "publications": "",
        "citedby" : "",
        "hindex": "",
        "i10-index": ""
    }

    
    result["publications"] = len(publications.find_all('tr')) - 2

    for item in citedby.select('tr:nth-child(n+1)'):
        result[item.find('a').find(text=True)] = int(item.find("td", {"class": "gsc_rsb_std"}).find(text=True))

    del result["i10-index"]

    if (res["citedby"] != result["citedby"]) or (res["hindex"] != result["h-icitedyndex"]) or (res["publications"] != result["publications"]):
        print(send_sms(result))
        f = open("result.json", "w")
        f.write(json.dumps(result))
        f.close()

    res["citedby"] = result["citedby"]
    res["hindex"] = result["hindex"]


    time.sleep(int(config('SLEEP_SECONDS')))
