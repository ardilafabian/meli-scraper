# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector


class MeliScraperPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

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
            price TEXT,
            reviews TEXT,
            free_fees TEXT
        )""")


    def process_item(self, items, spider):
        print('>>>>>>>> PIPELINE')
        print(items)
        self.store_db(items['items'])
        return items

    def store_db(self, items):
        for item in items:
            print('*'*10)
            print(item)
            self.curr.execute("""INSERT INTO meli_items VALUES (%s,%s,%s,%s)""", (
                item['name'],
                item['price'],
                item['reviews'],
                item['free_fees']
            ))
            self.conn.commit()