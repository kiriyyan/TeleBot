import json

import lxml.html
import requests
from lxml import etree
import redis

cache = redis.Redis(host = 'localhost', port = '6379', decode_responses=True)

def take_usd_to_rub():
    #пробуем достать из редис
    result = cache.get('usd')
    if result:
        return result
    try:
        html = requests.get('https://www.banki.ru/products/currency/cash/usd/moskva/').content
        tree = lxml.html.document_fromstring(html)
        result = tree.xpath("/html/body/div[2]/div/div/div/div/div[3]/div[2]/div[1]/div/section/div/div/div/div[2]/div[2]")
        cache.set(name = 'usd', value = result[0].text, ex = 3600)
    except requests.RequestException:
        return 'Error: Cant get access to USD'
    return(result[0].text)

def take_eur_to_rub():
    # пробуем достать из редис
    result = cache.get('eur')
    if result:
        return result
    try:
        html = requests.get("https://www.banki.ru/products/currency/cash/eur/moskva/").content
        tree = lxml.html.document_fromstring(html)
        result = tree.xpath("/html/body/div[2]/div/div/div/div/div[3]/div[2]/div[1]/div/section/div/div/div/div[2]/div[2]/text()")
        cache.set(name='eur', value=result[0], ex=3600)
    except requests.RequestException:
        return 'Error: Cant get access to EUR'
    return result[0]

def take_last_news():
    result = cache.get('posts')
    if result:
        result = json.loads(result)
        return f"\nНовостные сводки:\n📰{'\n\n📰'.join(result[i] for i in range(len(result)))}"
    try:
        html = requests.get('https://ria.ru/economy/').content
        tree = lxml.html.document_fromstring(html)
        result = tree.xpath("//a[contains(@class,'list-item__title color-font-hover-only')]/text()")
        cache.set('posts', json.dumps(result[:3]), ex = 3600)
    except requests.RequestException:
        return 'Error: Cant get access to NEWS'
    return f"\nНовостные сводки:\n📰{'\n\n📰'.join(result[i] for i in range(len(result[:3])))}"

