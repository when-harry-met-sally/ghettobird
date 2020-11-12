# from ghettobird import fly, iterate, transformer, TRANSFORM_parseJSONfromScript
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from pprint import pprint

# chromedriver_location = 'c:/chromedriver.exe'
# browser = webdriver.Chrome(executable_path=chromedriver_location)

# itinerary = {
#     "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/",
#     "flightpath": {
#         "header": "//*[@class='page-header']",
#         "jobs": [
#             {
#                 "@iterate": "//div[@class='job']",
#                 "title": ".//h4[@class='title']",
#                 "description": ".//h4[@class='description']",
#                 "dateposted": ".//div[@data-element-type='date']",
#                 "salary": "//h3[@id='salary-query']"
#             }
#         ]
#     }
# }

# fly(itinerary)
# pprint(itinerary["results"])

from lxml import html
import requests

def getTree(URL):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept-Language': 'en-gb',
        # 'Accept-Encoding': 'br, gzip, deflate',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        print(r.content)
        tree = html.fromstring(r.content)
        return tree
    except Exception as e:
        print(e)
        return None

tree = getTree("http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/")

print(tree.xpath("//div"))