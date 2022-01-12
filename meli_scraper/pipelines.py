# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector


class NumericalDataCleanupPipeline:

    def clean_price(self, str_price):
        price = str_price.replace(".", "")
        return int(price)

    def clean_fee(self, str_fee):
        fee = None
        if str_fee:
            fee = int(str_fee[6:7])
        return fee

    def clean_review(self, str_review):
        review = None
        if str_review:
            review = int(str_review)
        return review
    
    def process_item(self, items, spider):
        items_dict = items['items']
        for key in items_dict:
            item = items_dict[key]
            item['price'] = self.clean_price(item['price'])
            item['reviews'] = self.clean_review(item['reviews'])
            # item['free_fees'] = self.clean_fee(item['free_fees'])
        return items


class MySqlPipeline:

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host= 'localhost',
            user = 'root',
            password = 'admin123',
            database = 'meli_db'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS meli_items""")
        self.curr.execute("""CREATE TABLE meli_items(
            name TEXT,
            price INT,
            reviews INT,
            free_fees TEXT
        )""")

    def store_db(self, items_dict):
        for key in items_dict:
            item = items_dict[key]
            self.curr.execute("""INSERT INTO meli_items VALUES (%s,%s,%s,%s)""", (
                item['name'],
                item['price'],
                item['reviews'],
                item['free_fees']
            ))
            self.conn.commit()

    def process_item(self, items, spider):
        self.store_db(items['items'])
        self.conn.close()
        return items
