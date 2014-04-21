# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from HTMLParser import HTMLParser
import re


class StackoverflowPipeline(object):
    def process_item(self, item, spider):

        #extract id from url
        url_pattern = re.compile(".*/questions/(\d+)/.*")
        matched = url_pattern.match(item['url'])

        if matched:
            item['id'] = long(matched.group(1))

        item['title'] = item['title'][0]
        item['time'] = item['time'][0]

        #strip html tags
        item['question'] = self.strip_tags(item['question'][0])

        answers = list()
        for answer in item['answers']:
            answers.append(self.strip_tags(answer))
        item['answers'] = answers

        return item


    def strip_tags(self, html_str):

        html_str = html_str.strip()
        html_str = html_str.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(html_str)
        parser.close()
        return ''.join(result).strip().strip("\r\n")
