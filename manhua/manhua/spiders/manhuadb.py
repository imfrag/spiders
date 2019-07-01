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
        comic['comic_id'] = response.url.split('/')[-1]
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
            request.meta['comic_id'] = comic['comic_id']
            request.meta['id'] = 'vol-%s' % i
            res.append(request)
        yield comic

        for request in res:
            yield request

    def parse_vol(self, response: scrapy.http.Response):
        vol = VolItem()
        vol['vol_id'] = response.meta['id']
        vol['comic_id'] = response.meta['comic_id']
        vol['images'] = response.css('select#page-selector')[0].css('option::attr(value)').getall()
        vol['images'] = [response.urljoin(url) for url in vol['images']]
        yield vol

        for i, url in enumerate(vol['images'], start=1):
            request = scrapy.Request(url, callback=self.parse_page)
            request.meta['comic_id'] = vol['comic_id']
            request.meta['vol_id'] = vol['vol_id']
            request.meta['page'] = i
            yield request

    def parse_page(self, response: scrapy.http.Response):
        image_url = response.css('div#all div.text-center img.img-fluid::attr(src)').get()
        image_url = response.urljoin(image_url)
        image = ImageItem()
        image['comic_id'] = response.meta['comic_id']
        image['vol_id'] = response.meta['vol_id']
        image['page'] = response.meta['page']
        image['url'] = image_url
        yield image
