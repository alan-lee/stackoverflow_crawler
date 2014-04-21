from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from stackoverflow.items import StackoverflowItem


class StackoverflowSpider(CrawlSpider):
    name = 'stackoverflow'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['http://stackoverflow.com/?tab=hot']
    rules = [Rule(SgmlLinkExtractor(allow=["/questions/\d+/.*"]), 'parse_item')]

    def parse_item(self, response):
        sel = Selector(response)

        item = StackoverflowItem()
        item['url'] = response.url
        item['tags'] = sel.xpath("//div[@class='post-taglist']/a/text()").extract()
        item['title'] = sel.xpath("//div[@id='question-header']/h1/a/text()").extract()
        item['question'] = sel.xpath("//td[@class='postcell']//div[@class='post-text']").extract()
        item['time'] = sel.xpath("//td[@class='postcell']//div[@class='user-action-time']/span/@title").extract()
        item['answers'] = sel.xpath("//td[@class='answercell']//div[@class='post-text']").extract()

        return item