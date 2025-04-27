import scrapy


class LightnewparsSpider(scrapy.Spider):
    name = "lightnewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    # Настройки для экспорта в CSV
    custom_settings = {
        'FEEDS': {
            'lightnewpars.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True  # Перезаписать файл, если он существует
            }
        }
    }


    def parse(self, response):
        lights = response.css("div.WdR1o")
        for light in lights:
            yield {
                "name": light.css("div.lsooF span::text").get(),
                "price": f"{light.css('div.pY3d2 span::text').get()} руб." if light.css('div.pY3d2 span::text').get() else None,
                "link": light.css("a::attr(href)").get(),
            }