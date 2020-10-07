from pprint import pprint
from ghettobird import fly

routine = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            "iterate": "//div[@class='job']",
            "title": ".//h4[@class='title']",
            "description": ".//h4[@class='description']",
            "dateposted": ".//div[@data-element-type='date']",
            "salary": "//h3[@id='salary-query']",
        }]
    },
    "options": {
        "test": "test"
    }
}

fly(routine)
print('-----')
pprint(routine["results"])