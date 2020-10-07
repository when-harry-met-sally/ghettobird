from ghettobird import fly, iterate, transformer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint

# chromedriver_location = 'c:/chromedriver.exe'
# browser = webdriver.Chrome(executable_path=chromedriver_location)

def test(element):
    return "Avocado"

itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "links": {
            "path": ["//h4[@class='title']"],
            # transformer: test
        }
    },
}

fly(itinerary)
pprint(itinerary)