import scrapy

class PhoneSpider(scrapy.Spider):
    name = 'meli'
    start_urls = [
        'https://listado.mercadolibre.com.ar/celular-smarphones'
    ]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        samsung_filter_button_link = response.xpath('//h3[contains(@class, "__item__header") and contains(text(),"Samsung")]/parent::a/@href').get()
        if samsung_filter_button_link:
            yield response.follow(samsung_filter_button_link, callback=self.parse_items)
    
    def parse_items(self, response):
        print('*'*10)
        print('\n\n')
        titles = response.xpath('//li[contains(@class, "item")]/div[contains(@class, "wrapper")]/div/div[contains(@class, "content-wrapper")]/div[contains(@class, "title")]/a/h2/text()').getall()
        for title in titles:
            print(title)
        print('*'*10)
        print('\n\n')
