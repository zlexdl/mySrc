# -*- coding: utf-8 -*-
from datetime import datetime
# from redis import StrictRedis
import scrapy
import urllib
from TokenTransfers.commons import get_holder_name_mongodb
from TokenTransfers.items import TokenTopHistoryItem
from pymongo import MongoClient


class NebltopholderSpider(scrapy.Spider):
    name = 'NeblTopHolder'
    allowed_domains = ['explorer.nebl.io']
    start_urls = ['http://explorer.nebl.io/richlist/']
    # redis = StrictRedis(host='192.168.1.8', port=6379, db=0)
    conn = MongoClient('192.168.1.8', 27017)
    db = conn.token_address
    token_address = db.nebl
    rich_count = 50
    symbol = 'nebl'

    def parse(self, response):
        tokenTopHistoryItem = TokenTopHistoryItem()

        supply = self.get_supply()
        rank_tags = response.css("table.table tr > td:nth-child(1)::text").extract()
        quantity_tags = response.css("table.table tr > td:nth-child(3)::text").extract()
        address_tgas = response.css("table.table tr > td:nth-child(2)>a::text").extract()
        percentage_tags = response.css("table.table tr > td:nth-child(4)::text").extract()
        for index in range(0, self.rich_count):

            rank = rank_tags[index]
            quantity = quantity_tags[index + 2]
            address = address_tgas[index + 2]
            percentage = percentage_tags[index]
            # name = symbol + '_' + rank.zfill(3)

            name = get_holder_name_mongodb(self, address, rank)

            tokenTopHistoryItem['name'] = name
            tokenTopHistoryItem['symbol'] = self.symbol
            tokenTopHistoryItem['rank'] = rank
            tokenTopHistoryItem['quantity'] = quantity
            tokenTopHistoryItem['address'] = address
            tokenTopHistoryItem['percentage'] = float(percentage)
            tokenTopHistoryItem['timestamp'] = datetime.now()
            yield tokenTopHistoryItem

        tokenTopHistoryItem['name'] = 'Binance'
        tokenTopHistoryItem['symbol'] = self.symbol
        tokenTopHistoryItem['rank'] = 0
        tokenTopHistoryItem['quantity'] = float(quantity_tags[1])
        tokenTopHistoryItem['address'] = address_tgas[1]
        tokenTopHistoryItem['percentage'] = round(float(quantity_tags[1]) / supply, 2)
        tokenTopHistoryItem['timestamp'] = datetime.now()
        yield tokenTopHistoryItem

    def get_supply(self):
        url = 'http://explorer.nebl.io/ext/getmoneysupply'
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        result = response.read()
        return float(result.decode("utf-8"))

