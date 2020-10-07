from ghettobird import fly, iterate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint

chromedriver_location = 'c:/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver_location)

itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "options": {
        # "browser": browser
    },
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            iterate: "//div[@class='job']",
            "title": ".//h4[@class='title']",
            "description": ".//div[@class='description']",
            "dateposted": ".//div[@data-element-type='date']",
            "salary": "//h3[@id='salary-query']",
        }]
    },
}

fly(itinerary)
pprint(itinerary["results"])