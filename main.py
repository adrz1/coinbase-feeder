import logging
import os
import requests
import time
import json
import redis

DEBUG = os.environ.get("DEBUG", "").lower().startswith("y")

#TODO: config redis and notify if error
redis_conn = redis.Redis(charset="utf-8", decode_responses=True)

log = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)

def get_exchange_rates():#TODO: notify if X consecutive errors or expose metrics
    log.debug("Requesting exchange rates")
    r = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USD")
    content = r.text
    log.debug("Exchange rates received: {}...".format(content))
    return json.loads(content)

def push_currency_prices(exchange_rates):#TODO: notify if parse error
    base_currency = exchange_rates['data']['currency']
    out = {'base_currency': base_currency, 'marketplace': 'coinbase', 'prices': []}
    rates = exchange_rates['data']['rates']
    for currency in rates:
        rate = exchange_rates['data']['rates'][currency]
        out['prices'].append({'currency': currency, 'price': rate})
    log.debug(out)
    redis_conn.publish("currency_prices", json.dumps(out))

def loop(interval=1):
    while True:
        time.sleep(1)#TODO: pass as config
        push_currency_prices(get_exchange_rates())

if __name__ == "__main__":
    try:
        loop()
    except:
        log.exception("In coinbase-feeder loop:")
        log.error("Waiting 10s and restarting.")
        time.sleep(10)
