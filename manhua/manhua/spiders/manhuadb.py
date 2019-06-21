import scrapy


class ManhuaDBSpider(scrapy.Spider):
    name = 'manhuadb_com'

    def start_requests(self):
        start_urls = [
            'https://www.manhuadb.com/manhua/648',
        ]

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        pass

    def parse_detail(self, response: scrapy.http.Response):
        pass
