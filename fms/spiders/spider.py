import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import FmsItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class FmsSpider(scrapy.Spider):
	name = 'fms'
	start_urls = ['https://www.fmspks.dk/nyheder/rente-og-prisaendring/']

	def parse(self, response):
		post_links = response.xpath('//ul[@class="vert-nav"]/li/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="news-date"]/text()').get().strip()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="col col-md-9 news-article"]//text()[not (ancestor::h1)and not (ancestor::p[@class="news-date"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=FmsItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
