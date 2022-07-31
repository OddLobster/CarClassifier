import scrapy
import json

from car_scraper.items import CarScraperItem

class CarScraperSpider(scrapy.Spider):
    name = "car_scraper"

    def start_requests(self):
        self.num_pages = int(self.num_pages)
        start_urls = [f"https://www.willhaben.at/iad/gebrauchtwagen/auto/gebrauchtwagenboerse?sort=1&page={i}" for i in range(1, self.num_pages+1)]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def handle_car_data(self, response):
        item = CarScraperItem()
        item["title"] = response.css("div[class='Box-sc-wfmb7k-0 TMhyF']").css("h1[class='Text-sc-10o2fdq-0 bLnjhH']::text").get()
        top_header_div = "div[class='Box-sc-wfmb7k-0 emcHCy']" 
        head_detail_span = "span[class='Text-sc-10o2fdq-0 gDgZxY']::text"
        header_div = "div[class='Box-sc-wfmb7k-0 Flex-sc-1hx93kv-0 Stack___StyledFlex-sc-dqwciw-0 eDvenG thEqX']"
        item["registration_date"] = response.css(top_header_div).css(header_div).css("div[data-testid='ad-detail-teaser-attribute-0']").css(head_detail_span).get()
        item["mileage"] = response.css(top_header_div).css(header_div).css("div[data-testid='ad-detail-teaser-attribute-1']").css(head_detail_span).get()
        item["horse_power"] = response.css(top_header_div).css(header_div).css("div[data-testid='ad-detail-teaser-attribute-2']").css(head_detail_span).get()
        item["price"] = response.css("span[data-testid='contact-box-price-box-price-value-0']::text").get()
        item["address"] = response.css("div[data-testid='top-contact-box-address-box']").css("span::text").getall()

        car_data_titles = response.css("div[class='Box-sc-wfmb7k-0 dFLDMM']").css("div[data-testid='attribute-title']").css("span::text").getall()
        car_data_values = response.css("div[class='Box-sc-wfmb7k-0 dFLDMM']").css("div[data-testid='attribute-value']::text").getall()
        item["car_data"] = dict(zip(car_data_titles, car_data_values)) 

        item["description"] = response.css("div[data-testid='ad-description-Beschreibung']::text").getall()
        item["equipment"] = response.css("div[class='Box-sc-wfmb7k-0 Columns-sc-1kewbr2-0  UMtes']").css("div[data-testid='equipment-value']::text").getall()

        item["listing_type"] = response.css("p[class='Text-sc-10o2fdq-0 llBaNv']::text")[0].get()
        item["last_modified"] = response.css("span[data-testid='ad-detail-ad-edit-date-top']::text")[1].get()
        item["url"] = response.url

        json_data = json.loads(response.css("script[id='__NEXT_DATA__']::text").get())
        imgs = json_data["props"]["pageProps"]["advertDetails"]["advertImageList"]["advertImage"]
        urls = ""
        for i, img in enumerate(imgs):
            if i >= 3:
                break
            urls += img["mainImageUrl"] + ";"
        item["image_urls"] = urls
        yield item

    def parse(self, response):
        res = str(response.css("div[class='Box-sc-wfmb7k-0 gZawlG']").css("script[type='application/ld+json']")[0].get()).replace('<script type="application/ld+json">', "").replace('</script>', "")
        json_data = json.loads(res)
        for elem in json_data["itemListElement"]:
            url = "https://www.willhaben.at/"+elem["url"]
            yield scrapy.Request(url=url, callback=self.handle_car_data)