from ghettobird import fly, iterate, transformer, TRANSFORM_parseJSONfromScript
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint

chromedriver_location = 'c:/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver_location)


itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [
            {
                "@iterate": "//div[@class='job']",
                "title": ".//h4[@class='title']",
                "description": ".//h4[@class='description']",
                "dateposted": ".//div[@data-element-type='date']",
                "salary": "//h3[@id='salary-query']"
            }
        ]
    }
}


fly(itinerary)
pprint(itinerary["results"])