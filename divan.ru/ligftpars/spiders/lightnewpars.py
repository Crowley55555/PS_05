import scrapy


class LightnewparsSpider(scrapy.Spider):
    name = "lightnewpars"
    allowed_domains = ["https://divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lights = response.css("div.WdR1o")
        for light in lights:
            yield {
                "name": light.css("div.lsooF span::text").get(),
                "price": light.css("div.pY3d2 span::text").get(),
                "link": light.css("a::attr(href)").get(),
            }