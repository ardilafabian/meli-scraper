import scrapy

from ..items import MeliScraperItem

# title: //li[contains(@class, "item")]/div[contains(@class, "wrapper")]/div/div[contains(@class, "content-wrapper")]/div[contains(@class, "title")]/a/h2/text()

class PhoneSpider(scrapy.Spider):
    name = 'meli'
    start_urls = [
        'https://listado.mercadolibre.com.ar/celular-smarphones'
    ]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse_items(self, response, **kwargs):
        items = kwargs['items']

        print('*'*10)
        print('\n\n')
        # TODO: pensar si se puede traer sólo los FULL
        items_list = response.xpath('//div[@class="ui-search-result__content-wrapper"]')
        for idx, item_selection in enumerate(items_list):
            is_full = item_selection.xpath('.//span[@class="ui-search-item__fulfillment"]').get()
            if is_full:
                item = MeliScraperItem()
                item['name'] = item_selection.xpath('./div[contains(@class, "title")]/a/h2/text()').get()
                item['price'] = item_selection.xpath('.//span[@class="price-tag-fraction"]/text()').get()
                item['reviews'] = item_selection.xpath('.//span[@class="ui-search-reviews__amount"]/text()').get()
                item['free_fees'] = item_selection.xpath('.//div[contains(@class, "ui-search-item__group--price")]/span/text()').get()
                items.append(item)
                print(idx, item)
        
        """next_page_button_link = response.xpath('//div[@class="ui-search-pagination"]/ul/li[contains(@class, "__button--next")]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, self.parse_items, cb_kwargs={'items': items})"""
        
        print('*'*10)
        print('\n\n')

    def parse(self, response):
        # pages = int(getattr(self, 'pages', '5'))
        samsung_filter_button_link = response.xpath('//h3[contains(@class, "__item__header") and contains(text(),"Samsung")]/parent::a/@href').get()
        if samsung_filter_button_link:
            yield response.follow(samsung_filter_button_link, callback=self.parse_items, cb_kwargs={'items':[]})
