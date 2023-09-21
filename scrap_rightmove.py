import requests# 数据请求模块 第三方模块 pip install requests
import parsel # 数据解析模块
import re
import csv
import time
from bs4 import BeautifulSoup
import json
from geopy.geocoders import Nominatim
import os
for page in range(1, 100, 1):
    print('==========================Downloading page{}================================'.format(page))
    time.sleep(1)
    url = 'https://sz.lianjia.com/zufang/pg{}/#contentList'
    print(response.text)
    selector_1 = parsel.Selector(response.text)# 把获取到response.text 数据内容转成 selector 对象
    # 把获取到response.text 数据内容转成 selector 对象
    href = selector_1.css('div.propertyCard-details a::attr(href)').getall()

    href = ['https://www.rightmove.co.uk' + i for i in href]
    # 获取所有的房源链接
    for link in href:
        html_data = requests.get(url=link, headers=headers).text
        selector = parsel.Selector(html_data)
        # css选择器 语法
        # try:
        dit = {}
        soup = BeautifulSoup(html_data, 'lxml')
        title = soup.find(attrs={"itemprop": "name"})['content']
        dit['title'] = title
        property_type = selector.css('._1hV1kqpVceE9m-QrX_hWDN::text').get()
        dit['property_type'] = property_type
        price = selector.css('._1gfnqJ3Vtd1z40MlC0MzXu>span::text').get().replace('£', '')
        dit['price'] = price
        #house_area = selector.css('//dd[text()="sq"]::text').get()
        #house_area = soup.find("dd", text=re.compile("sq"))
        house_area = selector.css('._3vyydJK3KMwn7-s2BEXJAf::text').get()
        if house_area == None:
            house_area = selector.css('._3vyydJK3KMwn7-s2BEXJAf::text').get()
        else:
            house_area = selector.css('._3vyydJK3KMwn7-s2BEXJAf::text').get().replace('sq. m.)', '')
            house_area = house_area.replace('(', '')
        dit['house_area'] = house_area
        house_address = selector.css('h1._2uQQ3SV0eMHL1P6t5ZDo2q::text').get()
        dit['house_address'] = house_address
        google_maps_api_key = 'AIzaSyCCvPdzRUuGTojTUMlJh2mTa_youryBODM'
        url1 = f'https://maps.googleapis.com/maps/api/geocode/json?address={house_address}&key={google_maps_api_key}'
        response = requests.get(url1)
        json_data = json.loads(response.text)
        if json_data['status'] == 'ZERO_RESULTS':
            print('No results found')
            latitude = None
            longitude = None
        else:
            latitude = json_data['results'][0]['geometry']['location']['lat']
            dit['latitude'] = latitude
            longitude = json_data['results'][0]['geometry']['location']['lng']
            dit['longitude'] = longitude
        key_features = selector.css('._1uI3IvdF5sIuBtRIvKrreQ li::text').getall()
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        dit['key_features'] = key_features
        f = open('rightmove.csv', mode='a', encoding='utf-8', newline='')
        csv_writer = csv.DictWriter(f, fieldnames=['title', 'property_type', 'price', 'house_area', 'house_address', 'key_features', 'latitude', 'longitude'])
        csv_writer.writerow(dit)
        print(dit)
        print(title, property_type, price, house_area, house_address,key_features, latitude, longitude, sep='|')
csv_writer = csv.DictWriter(f, fieldnames=['title', 'property_type', 'price', 'house_area', 'house_address','key_features', 'latitude', 'longitude'])
csv_writer.writeheader()






