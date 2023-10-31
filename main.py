import requests
import selectorlib
import time
from functions import send_email

URL = "https://programmer100.pythonanywhere.com/tours/"
# "INSERT INTO events VALUES ('Tigers', 'Tigers City', '2023.10.10')"
# "SELECT * FROM events WHERE date='2023.10.15'"

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
    with open('data.txt', 'a') as file:
        file.write(extracted + "\n")        


def read_extracted(extracted):
    with open('data.txt', 'r') as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        content = read_extracted(extracted)
        print(extracted)
        
        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                # send_email(message="Hey, new event was found!")
                
        time.sleep(10)
