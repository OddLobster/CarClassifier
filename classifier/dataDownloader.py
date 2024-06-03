import sqlite3 as sql   
import urllib.request


def getCarData():
    links = []
    with sql.connect("../car.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, image_urls FROM car")
        rows = cur.fetchall()
        for row in rows:
            links.append([row[0], [x for x in row[1].split(";") if x != ""]])   
    return links

def main():
    data = getCarData()
    print()

if __name__ == "__main__":
    main()