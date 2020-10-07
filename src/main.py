from ghettobird import fly, iterate, transformer, TRANSFORM_parseJSONfromScript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint

chromedriver_location = 'c:/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver_location)

def test(element):
    return "Avocado"

itinerary = {
            "url": "https://www.glassdoor.com/Overview/Working-at-UniGroup-EI_IE3422.11,19.htm",
            "flightpath": {
                "ratings": {
                    "path": "//script[@type='application/ld+json']",
                    TRANSFORM_parseJSONfromScript: {
                        "rating": ["ratingValue"]
                    }
                }
            },
}

fly(itinerary)
pprint(itinerary["results"])