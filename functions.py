import requests
from decouple import config, Csv


def send_sms(message):
    url = config('SMS_API')
    # TODO: Custom messages
    pm = f'My dear Nila,\nI sincerely congratulate you on your new achievement\nI mean about your {message["publications"]} Publications, H-index {message["hindex"]} and Citations {message["citedby"]}\nI am proud to say that I am happy to be by your side in your professional advancement\nI love you, Javad'
    headers = {
        'apikey': config('SMS_SECRET'),
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    for receptor in config('SMS_RECEPTORS', cast=Csv()):
        payload = f"message={pm}&sender={config('SMS_SENDER')}&receptor={receptor}"
        response = requests.request("POST", url, data=payload, headers=headers)
    
    return response.text
