import time
import sqlite3 as sql
import subprocess
import datetime 
import logging

logging.basicConfig(filename="car_scrape.log", level=logging.INFO)
SCRAPE_INTERVAL = int(60*60*0.25) #in seconds

def main():
    total_scrapes_today = 0
    sum_new_entries = 0 
    total_time = 0
    pages_to_scrape = 25
    with sql.connect('car.db') as conn:
        cursor = conn.cursor()
        while True:
            print("Scrapes:", total_scrapes_today)
            logging.info(" Begin Scrape at: " +  str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
            entries_before = cursor.execute('''SELECT COUNT(*) FROM car''').fetchone()[0]

            if total_scrapes_today > 0:
                pages_to_scrape = 5

            time_start = time.time()
            subprocess.call(["scrapy", "crawl", "car_scraper", "-a", f"num_pages={pages_to_scrape}"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            time_end = time.time()
            print("Scrape took:", time_end - time_start)
            total_time += time_end - time_start
            entries_after = cursor.execute('''SELECT COUNT(*) FROM car''').fetchone()[0]
            if total_scrapes_today % 4 == 0:
                logging.info(" Total entries: " + str(entries_after))
            logging.info(" New entries: " + str(entries_after - entries_before))
            sum_new_entries += entries_after - entries_before

            total_scrapes_today += 1
            time.sleep(SCRAPE_INTERVAL)
            total_time += time_end - time_start
            if total_time >= 60*60*24:
                logging.info(" New entries last 24 hours: " + str(sum_new_entries))
                sum_new_entries = 0
                total_scrapes_today = 0



if __name__ == "__main__":
    main()