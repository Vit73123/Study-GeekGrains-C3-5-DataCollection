import scrapy


class CountriesSpider(scrapy.Spider):
    name = "countries"
    allowed_domains = ["tradingeconomics.com"]
    start_urls = ["https://tradingeconomics.com/country-list/inflation-rate?continent=world"]

    def parse(self, response):
        countries = response.xpath("//td/a")
        for i, country in enumerate(countries):
            name = country.xpath(".//text()").get().strip()
            link = country.xpath(".//@href").get()
            # absolute_url = response.urljoin(link)
            # yield scrapy.Request(url=absolute_url)
            if i > 1: break
            yield response.follow(url=link,
                                  callback=self.parse_country,
                                  meta={'country_name': name})

    def parse_country(self, response):
        rows = response.xpath("//div[@id='ctl00_ContentPlaceHolder1_ctl00_ctl01_PanelComponents']//tr[@class='datatable-row']")
        for row in rows:
            related = row.xpath(".//td/a/text()").get().strip()
            last = float(row.xpath(".//td[2]/text()").get())
            previous = row.xpath(".//td[3]/text()").get()
            name = response.request.meta['country_name']
            yield {
                'country_name': name,
                'related': related,
                'last': last,
                'previous': previous,
            }
