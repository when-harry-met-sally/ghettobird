from ghettobird import master_method, fly
from pprint import pprint #prettier print statements

routine = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            "iterate": "//div[@class='job']", #iterates through job containers
            "title": ".//h4[@class='title']",
            "dateposted": ".//div[@data-element-type='date']",
            "salary": "//h3[@id='salary-query']",
        }]
    }
}

fly(routine)
pprint(routine["results"])