# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from manhua.items import *
import os
import requests


class ManhuaPipeline(object):

    def process_item(self, item: scrapy.Item, spider):
        path = os.path.abspath('.')
        path = os.path.join(path, 'manhua')
        if not os.path.exists(path):
            os.mkdir(path)

        comic_path = ''
        if isinstance(item, ManhuaItem):
            comic_path = os.path.join(path, item.get('id'))
        if not os.path.exists(comic_path):
            os.mkdir(comic_path)

        if isinstance(item, ManhuaItem):
            thumbnail_path = os.path.join(comic_path,
                                          'thumbnail.%s' % item['thumbnail'].split('.')[-1])
            if not os.path.exists(thumbnail_path):
                with open(thumbnail_path, 'wb') as f:
                    f.write(requests.get(item['thumbnail']).content)

            with open(os.path.join(comic_path, '%s.inf' % item['id']), 'wb') as f:
                info = ('Title: %s\n'
                        'Original Title: %s\n'
                        'Author: %s\n'
                        'State: %s\n'
                        'Duration: %s\n'
                        'Summary: %s\n'
                        'Comic URL: %s\n' % (item['title'],
                                       item['original_title'],
                                       item['author'],
                                       item['state'],
                                       item['duration'],
                                       item['summary'],
                                       item['url'])).encode('utf-8')
                f.write(info)
                for i, url in item['vols'].items():
                    f.write(('%s:\t%s\n' % (i, url)).encode('utf-8'))
        elif isinstance(item, VolItem):
            pass

        return item
