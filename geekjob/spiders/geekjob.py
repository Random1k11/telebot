import re

import scrapy

from geekjob.items import GeekjobItem


class QuotesSpider(scrapy.Spider):
    name = "geek"
    count = 1

    def start_requests(self):
        url = 'https://geekjob.ru/vacancies'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        vacancies_links = response.xpath('//p[@class="truncate vacancy-name"]/a/@href').extract()
        amount_of_pages = response.xpath(
                '//section[@class="col s12 m12 center-align"]/p[2]//text()'
            ).extract_first()
        amount_of_pages = int(re.search(r'\d+', amount_of_pages).group())
        for link in vacancies_links:
            yield scrapy.Request(url='https://geekjob.ru' + link, callback=self.get_info)
        if self.count <= amount_of_pages:
            self.count += 1
            yield scrapy.Request(url='https://geekjob.ru/vacancies/' + str(self.count), callback=self.parse)

    def get_info(self, response):
        link = response.url
        title = response.xpath('//section[@class="col s12 m10 main"]//h1/text()').extract_first()
        description = ''.join(response.xpath(
            '//div[@class="description"]//text()'
        ).extract())

        item = GeekjobItem()
        item['link'] = link
        item['title'] = title
        item['description'] = description

        yield item
