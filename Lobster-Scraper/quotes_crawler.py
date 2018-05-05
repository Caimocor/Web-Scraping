import scrapy
from scrapy.loader import ItemLoader


class QuotesItem(scrapy.Item):

    text = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()



class QuotesCrawler(scrapy.Spider):
    name = 'quotes-js'


    def start_requests(self):
        yield scrapy.splashrequest(URL)(
            url = 'http://quotes.toscrape.com/js',
            callback = self.parse,

        )

    def parse(self, response):

        item  = QuotesItem()
        for quote in response.css('div.quote'):
            item['text'] = quote.css('span.text::text').extract_first()
            item['author'] = quote.css('span small::text').extract_first()
            item['tags'] = quote.css('div.tags a.tag::text').extract()
            return item

