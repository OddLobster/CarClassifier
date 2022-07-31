import sqlite3 as sql   
import urllib.request
#urllib.request.urlretrieve("http://www.digimouth.com/news/media/2011/09/google-logo.jpg", "local-filename.jpg")
from PIL import Image, ImageOps
import time 

car_brands = []

def initCarBrands():
    global car_brands
    with open("../CarBrandScraper/car_brands/car_brands.txt") as file:
        for line in file:
            car_brands.append(line.strip())
    car_brands = set(car_brands)

def getBrandNameFromTitle(title):
    for part in title.split(" "):
        if part.strip().lower() in car_brands:
            if part == "aston":
                return "aston-martin"
            elif part == "alfa":
                return "alfa-romeo"
            else:
                return part
    return "Error" + " " + title

def getCarData():
    links = []
    with sql.connect("../car.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, image_urls FROM car")
        rows = cur.fetchall()
        for row in rows:
            links.append([getBrandNameFromTitle(row[0]), [x for x in row[1].split(";") if x != ""]])   
    return links

def downloadImages(links):
    size = (300,300)
    for link in links:
        print("Downloading images from:", link[1])
        for image_url in link[1]:
            try:
                name = "data/" + link[0].lower() + "_" + image_url.split("/")[-1].replace("_", "").replace("-", "")
                urllib.request.urlretrieve(image_url, name)
                img = Image.open(name)
                resized = img.resize(size, Image.ANTIALIAS)
                resized.save(name)
                time.sleep(2)
            except:
                print("Failed to download:", image_url)
                print("Waiting for 1 minute...")
                time.sleep(60)

def main():
    initCarBrands()
    data = getCarData()
    downloadImages(data)

if __name__ == "__main__":
    main()