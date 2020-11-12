from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ghettobird import fly, iterate, transformer, TRANSFORM_parseJSONfromScript
from pprint import pprint

chromedriver_location = 'c:/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver_location)

test_cases = [{
    "id": 1,
    "description": "tree_method with iterate. no transformers. no paths. no options.",
    "itinerary": {
        "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
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
    },
    "correct": {'header': 'Jobs in St. Louis, Missouri',
                'jobs': [{'dateposted': '(Date Posted: 9/9/2020)',
                          'description': 'Need a master of React Native, a man or woman with '
                          'gumption, who can lead a team.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Senior Software Dev'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a trained agility coach who can combat '
                          'followers of the waterfall method. Zealotry '
                          'required.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Agile Coach'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a remote Java whiz who can do build a bowling '
                          'scoring app.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Software Engineer'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a spry, young developer who can juggle.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Junior Software Dev'},
                         {'dateposted': '(Date Posted: 9/9/2020)',
                          'description': 'Need an athetlic ping pong player.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Ping Pong Player'}]}
},
    {
    "id": 2,
    "description": "selenium_method with iterate. no transformers. no paths.",
    "itinerary": {
        "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
        "options": {
            "browser": browser,
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
    },
    "correct": {'header': 'Jobs in St. Louis, Missouri',
                'jobs': [{'dateposted': '(Date Posted: 9/9/2020)',
                          'description': 'Need a master of React Native, a man or woman with '
                          'gumption, who can lead a team.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Senior Software Dev'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a trained agility coach who can combat '
                          'followers of the waterfall method. Zealotry '
                          'required.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Agile Coach'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a remote Java whiz who can do build a bowling '
                          'scoring app.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Software Engineer'},
                         {'dateposted': '(Date Posted: 9/8/2020)',
                          'description': 'Need a spry, young developer who can juggle.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Junior Software Dev'},
                         {'dateposted': '(Date Posted: 9/9/2020)',
                          'description': 'Need an athetlic ping pong player.',
                          'salary': 'Salary Range: 10,000 - 100,000',
                          'title': 'Ping Pong Player'}]}
},
    {
    "id": 3,
    "description": "selenium_method with TRANSFORM_parseJSONfromScript. Uses transform function that takes arguments as directions to the relevant data",
    "itinerary": {
        "url": "https://www.glassdoor.com/Overview/Working-at-UniGroup-EI_IE3422.11,19.htm",
        "flightpath": {
            "ratings": {
                "path": "//script[@type='application/ld+json']",
                TRANSFORM_parseJSONfromScript: {
                        "rating": ["ratingValue"]
                }
            }
        },
    },
    "correct": {'ratings': {'rating': '3.5'}}
}]


def test():
    total_cases = len(test_cases)
    failed = 0
    for case in test_cases:
        itinerary = case["itinerary"]
        fly(itinerary)
        if itinerary["results"] == case["correct"]:
            print(" - (#{}) Case passed.".format(case["id"]))
        else:
            print(" - (#{}) Case failed.".format(case["id"]))
            print("---- Expected ----")
            pprint(case["correct"])
            print("---- Received ----")
            pprint(itinerary["results"])
            print("---- Log ---------")
            pprint(itinerary)
            failed += 1
    print("---------------------------------------------------")
    if failed == 0:
        print("Success: All cases passed.")
    else:
        print("Failure: {} out of {} cases failed.".format(failed, total_cases))
    print("---------------------------------------------------")


if __name__ == '__main__':
    test()
