# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import time

from manhua.manhua.items import *


class ManhuaPipeline(object):

    def process_item(self, item: scrapy.Item, spider):
        path = os.path.abspath('.')
        path = os.path.join(path, 'manhua')
        if not os.path.exists(path):
            os.mkdir(path)

        comic_path = os.path.join(path, item.get('comic_id'))
        if not os.path.exists(comic_path):
            os.mkdir(comic_path)

        if item.get('vol_id', ''):
            vol_path = os.path.join(comic_path, item.get('vol_id'))
            if not os.path.exists(vol_path):
                os.mkdir(vol_path)

        if isinstance(item, ManhuaItem):
            thumbnail_path = os.path.join(comic_path,
                                          'thumbnail.%s' % item['thumbnail'].split('.')[-1])
            with open(thumbnail_path, 'wb') as f:
                f.write(requests.get(item['thumbnail']).content)

            with open(os.path.join(comic_path, '%s.inf' % item['comic_id']), 'wb') as f:
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
            vol_id = item['vol_id']
            vol_path = os.path.join(comic_path, vol_id)
            if not os.path.exists(vol_path):
                os.mkdir(vol_path)
            with open(os.path.join(vol_path, 'pages'), 'wb') as f:
                for i, url in enumerate(item['images'], start=1):
                    f.write(('Page-%s: %s\n' % (i, url)).encode('utf-8'))
        elif isinstance(item, ImageItem):
            t = item['url'].split('.')[-1]
            with open(os.path.join(vol_path, 'Page-%s.%s' % (item['page'], t)), 'wb') as f:
                f.write(requests.get(item['url']).content)
                time.sleep(1)

        return item
