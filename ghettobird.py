from pprint import pprint
from lxml import html
import requests
import re

#idea one
#library that assists in scraping, does try catch shit for you, iterates for you

#idea two
#library that finds convenient xpath for you
#arg1 = item in list you are trying to scrape, arg2 = item in list you are trying to scrape, num of items 

def getTree(URL):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept-Language': 'en-gb',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        tree = html.fromstring(r.content.decode("utf-8", "replace"))
        return tree
    except:
        return None

def getText(element):
    return element.text

structure = {
    "jobtitle": {
        "xpath": "//div[@class='cmp-JobListItem-title']",
        "transform": getText,
    },
    "time": {
        "xpath": "//div[@class='cmp-JobListItem-timeTag']",
        "transform": getText,
    }
}

def main():
    def getCouplings(structure):
        couplings = []
        length = []
        keys = structure.keys()
        for field in keys:
            try:
                elements = tree.xpath(structure[field]["xpath"])
                structure[field]["elements"] = elements
                length = len(elements)
            except:
                print(field + " not found.")
        for l in range(0, length):
            obj = {}
            for field in keys:
                obj[field] = structure[field]["transform"](structure[field]["elements"][l])
            couplings.append(obj)
        pprint(couplings)

    url = "https://de.indeed.com/cmp/Getyourguide/jobs"
    tree = getTree(url)
    getCouplings(structure)

    


main()
