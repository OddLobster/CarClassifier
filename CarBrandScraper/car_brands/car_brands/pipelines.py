# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

class CarBrandsPipeline:
    def __init__(self):
        self.file = open("car_brands.txt", "w+", encoding="utf-8")

    def __del__(self):
        self.file.close()

    def process_item(self, item, spider):
        for name in item["names"]:
            self.file.write(name + "\n")
