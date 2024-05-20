import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from L06_Scrapy_Media.hw.unsplashparser.items import UnsplashparserItem

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.query = kwargs.get('query')
        self.start_urls = [f"https://unsplash.com/t/{self.query}"]

    def parse(self, response):
        links = response.xpath("//a[@itemprop='contentUrl']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_image)

    def parse_image(self, response):
        # print()
        loader = ItemLoader(item=UnsplashparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_value('url', response.url)
        loader.add_value('category', self.query)
        loader.add_xpath('photos', "//div[@class='SuKTa QQXuL']//div[@class='WxXog']//img/@srcset")
        yield loader.load_item()