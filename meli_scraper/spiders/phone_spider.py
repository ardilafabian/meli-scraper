import scrapy

from ..items import MeliScraperItem

# title: //li[contains(@class, "item")]/div[contains(@class, "wrapper")]/div/div[contains(@class, "content-wrapper")]/div[contains(@class, "title")]/a/h2/text()

# solo los fulll: //span[@class="ui-search-item__fulfillment"]/ancestor::div[@class="ui-search-result__content-wrapper"]

class PhoneSpider(scrapy.Spider):
    name = 'meli'
    start_urls = [
        'https://listado.mercadolibre.com.ar/celular-smarphones'
    ]
    custom_settings = {
        'FEED_URI': 'items.json',
        'FEED_FORMAT': 'json',
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def gen_key_item(self, item):
        """
        Unique key that is necessary because there're products
        with the same name but diff prices
        """
        return f'{item["name"]}-{item["price"]}'

    def parse_items(self, response, **kwargs):
        items = kwargs['items']
        pages = kwargs['pages']
        quantity = kwargs['quantity']

        # Retrive just FULL items instead of the whole list
        items_list = response.xpath('//span[@class="ui-search-item__fulfillment"]/ancestor::div[@class="ui-search-result__content-wrapper"]')
        for item_selection in items_list:
            item = MeliScraperItem()
            item['name'] = item_selection.xpath('./div[contains(@class, "title")]/a/h2/text()').get()
            item['price'] = item_selection.xpath('.//span[@class="price-tag-fraction"]/text()').get()
            item['reviews'] = item_selection.xpath('.//span[@class="ui-search-reviews__amount"]/text()').get()
            item['free_fees'] = item_selection.xpath('.//div[contains(@class, "ui-search-item__group--price")]/span/text()').get()

            key = self.gen_key_item(item)
            if not key in items:
                quantity += 1
                items[key] = item

        next_page_button_link = response.xpath('//div[@class="ui-search-pagination"]/ul/li[contains(@class, "__button--next")]/a/@href').get()
        if next_page_button_link and pages > 0:
            yield response.follow(next_page_button_link, self.parse_items, cb_kwargs={'items': items, 'pages': pages - 1, 'quantity': quantity})
        else: 
            yield {
                'quantity': quantity,
                'items':items
            }

    def parse(self, response):
        pages = int(getattr(self, 'pages', '5'))
        samsung_filter_button_link = response.xpath('//h3[contains(@class, "__item__header") and contains(text(),"Samsung")]/parent::a/@href').get()
        if samsung_filter_button_link:
            yield response.follow(samsung_filter_button_link, callback=self.parse_items, cb_kwargs={'items':{}, 'pages':pages, 'quantity': 0})
