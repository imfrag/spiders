import scrapy

from manhua.items import *


class ManhuaDBSpider(scrapy.Spider):
    name = 'manhuadb_com'

    def start_requests(self):
        start_urls = [
            'https://www.manhuadb.com/manhua/648',
        ]

        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        comic = ManhuaItem()
        comic['id'] = response.url.split('/')[-1]
        comic['url'] = response.urljoin(response.url)
        comic['thumbnail'] = response.urljoin(response.css('div.cover img::attr(src)').get())
        comic['title'] = response.css('td.comic-titles::text').get()
        comic['original_title'] = response.css('td.comic-original-titles::text').get()
        comic['author'] = response.css('ul.creators li a::text').getall()
        comic['summary'] = response.css('p.comic_story::text').get()
        comic['state'] = response.css('a.comic-pub-state::text').get()
        comic['duration'] = '-'.join(response.css('td.pub-duration a::text').getall())
        comic['vols'] = dict()

        res = []
        vol_urls = response.css('ol.links-of-books.num_div li a::attr(href)').getall()
        for i, url in enumerate(vol_urls, start=1):
            comic['vols']['vol-%s' % i] = response.urljoin(url)
            request = scrapy.Request(response.urljoin(url), callback=self.parse_vol)
            request.meta['comic_id'] = comic['id']
            res.append(request)
        yield comic

        # for request in res:
        #     yield request

    def parse_vol(self, response: scrapy.http.Response):
        vol = VolItem()
        pass
