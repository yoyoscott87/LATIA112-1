import scrapy

class StormSpider(scrapy.Spider):
    name = 'storm'
    allowed_domains = ['storm.mg']
    start_urls = ['https://www.storm.mg/life-category/s24251/']

    def parse(self, response):
        for page in range(1, 6):
            url = f'https://www.storm.mg/life-category/s24251/{page}'
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        for card_title in response.css('.card_title'):
            title = card_title.css('::text').get().strip()
            print(title)
            yield {
                'title': title
            }
