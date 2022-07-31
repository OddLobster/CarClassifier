# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3 as sql  

class CarScraperPipeline:
    def __init__(self) -> None:
        self.connection = sql.connect('car.db')
        with self.connection:
            cur = self.connection.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS car (id INTEGER PRIMARY KEY, 
                                                            title TEXT,
                                                            price INTEGER,
                                                            mileage INTEGER,
                                                            horse_power INTEGER,
                                                            address TEXT,
                                                            registration_date TEXT,
                                                            description TEXT,
                                                            equipment TEXT,
                                                            listing_type TEXT,
                                                            
                                                            previous_owner INTEGER,
                                                            fuel_type TEXT,
                                                            transmission TEXT,
                                                            engine_type TEXT,
                                                            condition TEXT,
                                                            seats INTEGER,
                                                            car_type TEXT,
                                                            color TEXT,
                                                            doors INTEGER,
                                                            last_modified TEXT,
                                                            url TEXT,
                                                            image_urls TEXT
                                                            )""")

    def process_item(self, item, spider):
        try:
            previous_owner = item["car_data"]["Vorbesitzer"]
        except:
            previous_owner = -1

        try:
            fuel_type = item["car_data"]["Treibstoff"]
        except:
            fuel_type = ""

        try:
            transmission = item["car_data"]["Getriebeart"]
        except:
            transmission = ""

        try:
            engine_type = item["car_data"]["Antrieb"]
        except:
            engine_type = ""

        try:
            condition = item["car_data"]["Zustand"]
        except:
            condition = ""
        
        try:
            seats = item["car_data"]["Anzahl Sitze"]
        except:
            seats = -1
        
        try:
            car_type = item["car_data"]["Fahrzeugtyp"]
        except:
            car_type = ""
        
        try:
            color = item["car_data"]["Außenfarbe"]
        except:
            color = ""
        
        try:
            doors = item["car_data"]["Anzahl Türen"]
        except:
            doors = -1
    
        with self.connection:
            cur = self.connection.cursor()
            duplicate_query = 'SELECT id FROM car WHERE title = ? AND price = ? AND mileage = ? AND horse_power = ? AND address = ? AND registration_date = ? AND description = ? AND equipment = ? AND listing_type = ? AND previous_owner = ? AND fuel_type = ? AND transmission = ? AND engine_type = ? AND condition = ? AND seats = ? AND car_type = ? AND color = ? AND doors = ? AND last_modified = ?'
            cur.execute(duplicate_query, (item["title"], item["price"], item["mileage"].replace(".", ""), item["horse_power"], ";".join(item['address']), item["registration_date"], 
                        "".join(item['description']), ";".join(item['equipment']), item["listing_type"], previous_owner, fuel_type, transmission, engine_type, condition, 
                                                seats, car_type, color, doors, item["last_modified"]))
            if cur.fetchone() is None:
                cur.execute("""INSERT INTO car (title, price, mileage, horse_power, address, 
                                                registration_date, description, equipment, listing_type, 
                                                previous_owner, fuel_type, transmission, engine_type, condition, 
                                                seats, car_type, color, doors, last_modified, url, image_urls)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (item['title'],
                                item['price'],
                                item['mileage'].replace(".", ""),
                                item['horse_power'],
                                ";".join(item['address']),
                                item['registration_date'],
                                "".join(item['description']),
                                ";".join(item['equipment']),
                                item['listing_type'],
                                previous_owner, 
                                fuel_type, 
                                transmission, 
                                engine_type, 
                                condition, 
                                seats, 
                                car_type, 
                                color, 
                                doors,
                                item['last_modified'],
                                item['url'],
                                item['image_urls']))
            else:
                print("Duplicate found")
        return item
