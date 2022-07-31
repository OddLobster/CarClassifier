# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CarScraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    mileage = scrapy.Field()
    horse_power = scrapy.Field()
    address = scrapy.Field()
    registration_date = scrapy.Field()
    description = scrapy.Field()
    equipment = scrapy.Field()
    listing_type = scrapy.Field()       #commercial or private
    last_modified = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()

    car_data = scrapy.Field()
    
