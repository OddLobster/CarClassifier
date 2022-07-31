import scrapy
from car_brands.items import CarBrandsItem

class CarBrandSpider(scrapy.Spider):
    name = "car_brands"
    
    def start_requests(self):
        start_url = "https://www.car.info/en-se/brands"
        yield scrapy.Request(start_url, callback=self.parse)

    def parse(self, response):
        brands = response.css("ul[class='row list-unstyled w-100 px-2']")[0].css("a::text").getall()[:-16]
        urls = response.css("ul[class='row list-unstyled w-100 px-2']")[0].css("a::attr(href)").getall()[:-19]
        item = CarBrandsItem()
        item["names"] = brands
        item["urls"] = urls
        yield item

