import scrapy
import ipdb
import re
from time import sleep

class Tecmundo (scrapy.Spider):
    name = 'tecmundo'
    start_urls = ['https://www.tecmundo.com.br/novidades']

    # def parse(self, response):
    #     links = response.xpath('//nav//ul//li/a[re:test(@href, "novidades")]/@href')

    #     for link in links:
    #         yield scrapy.Request(
    #             link,
    #             callback=self.parse_category
    #             )

    def parse(self, response):
        news = response.css('.tec--card__title__link::attr(href)').getall()

        for new_url in news:
            yield scrapy.Request(
                new_url,
                callback=self.parse_new
            )
        
        pages_urls = response.css('a.tec--btn::attr(href)').get()
        numPagina = re.search (r'\d+', pages_urls)
        numPagina = int(numPagina[0])
        print(numPagina)
        sleep(2)
        limitPages = 10

        if numPagina < limitPages:
            yield scrapy.Request(pages_urls,callback=self.parse)

    def parse_new(self, response):
        title = response.css('h1.tec--article__header__title::text').get()
        date = response.css('time::attr(datetime)').getall()[0]
        time = response.css('time strong::text').get()

        yield {
            'title': title,
            'date': date,
            'time': time,
            'url': response.url
        }