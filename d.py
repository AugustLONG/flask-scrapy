# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle

from scrapy_my.items import doubanBookItem
from scrapy.exceptions import CloseSpider


class doubanBookSpider(CrawlSpider):
	name = "doubanBook"
	allowed_domains = ["douban.com"]
	start_urls = [u"http://www.douban.com/tag/科幻/?focus=book"]

	rules = [
		Rule(sle(allow = ("book.douban.com/subject/[\d+]/?(.*?)$")), callback = 'parse_book')
	]

	global items
	items = []

	def parse_book(self, response):

		sel = Selector(response)
		sel = sel.xpath('//')

		for sel in sels:
			item = doubanBookItem()
			item['title'] = sel.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
			item['author'] = sel.xpath('//*[@id="info"]/span[1]/a').extract()
			item['intro_content'] = sel.xpath('//*[@id="link-report"]/div[1]/div/p[1]/text()').extract()
			item['intro_author'] = sel.xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/div/p[1]').extract()

			items.append(item)
			print('success add one pagecontent')

			if len(items) > 30:
				raise CloseSpider('enough')

			return items







