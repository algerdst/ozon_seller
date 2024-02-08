import csv

import requests
import json

with open('login_data.txt', 'r', encoding='utf-8') as file:
    data = [i for i in file]
client_id = data[0].replace('\n', '')
api_key = data[1].replace('\n', '')

headers = {
        "Client-Id": client_id,
        "Api-Key": api_key
    }

def get_data_ozon():
    print("[+][+][+][+]СБОР АРТИКУЛОВ ТОВАРОВ[+][+][+]")

    last_id = ''
    items = {}
    while True:

        if last_id == '':
            payload = json.dumps({
                "limit": 1000,
            })
        else:
            payload = json.dumps({
                "limit": 1000,
                "last_id": last_id
            })

        url = "https://api-seller.ozon.ru/v2/product/list"
        # Получение информации об отчёте
        resp_data = requests.post(url, headers=headers, data=payload).json()
        if resp_data['result']['items'] == []:
            break
        last_id = resp_data['result']['last_id']
        for i in resp_data['result']['items']:
            items[i['product_id']] = i['offer_id']
    print(F"[+][+][+][+]СОБРАНО {len(items)} АРТИКУЛОВ[+][+][+]")
    return items


items = get_data_ozon()


def get_data_product():
    print("[+][+][+][+]СБОР ИНФОРМАЦИИ О ТОВАРАХ[+][+][+]")
    count = 0
    items_quantity = len(list(items))
    with open('результат.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Артикул', 'Штрихкод', 'Цена для покупателя', 'min_ozon_price', 'old_price'
                         , 'premium_price', 'price_2', 'recommended_price', 'min_price'])
    url = "https://api-seller.ozon.ru/v2/product/info"
    for key in list(items):
        payload = json.dumps({
            "offer_id": items[key],
            "product_id": key,
        })

        resp_data = requests.post(url, headers=headers, data=payload).json()
        barcode = resp_data['result']['barcode']
        price = resp_data['result']['marketing_price'].replace('.', ',')
        min_ozon_price=resp_data['result']['min_ozon_price'].replace('.', ',')
        old_price=resp_data['result']['old_price'].replace('.', ',')
        premium_price=resp_data['result']['premium_price'].replace('.', ',')
        price_2=resp_data['result']['price'].replace('.', ',')
        recommended_price=resp_data['result']['recommended_price'].replace('.', ',')
        min_price=resp_data['result']['min_price'].replace('.', ',')
        count += 1
        print(f"[+]ОСТАЛОСЬ СОБРАТЬ {items_quantity - count} товаров[+]")
        with open('результат.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([items[key], barcode, price, min_ozon_price, old_price, premium_price, price_2, recommended_price,
                             min_price])


get_data_product()
