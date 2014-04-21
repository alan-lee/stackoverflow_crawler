# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class StackoverflowItem(Item):
    id = Field()
    url = Field()
    category = Field()
    tags = Field()
    title = Field()
    question = Field()
    time = Field()
    answers = Field()
