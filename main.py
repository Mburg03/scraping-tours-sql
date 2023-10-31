import requests
import selectorlib
import time
import sqlite3
from functions import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
# "INSERT INTO events VALUES ('Tigers', 'Tigers City', '2023.10.10')"
# "SELECT * FROM events WHERE date='2023.10.15'"
connection = sqlite3.connect("./data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    
    return value


def store(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read_extracted(extracted):
    row = extracted.split(',')
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", 
                   (band, city, date))
    rows = cursor.fetchall()
    return rows

    
if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        
        if extracted != "No upcoming tours":
            row = read_extracted(extracted)
            if not row:
                store(extracted)
                send_email(message="Hey, new event was found!")
                
        time.sleep(10)
