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

#transform functions
def getText(element):
    return element.text
#----------------------

def getCouplings(tree, structure):
    couplings = [] 
    lengths = 0 #the amount of entries on the page.
    keys = structure.keys() #fields: jobtitle, dateposted

    #grabs an array of elements for each field in the structure object.
    #jobtitle is given an array of all jobtitle elements
    #dateposted is given an array fo all datepoted elements
    for field in keys:
        try:
            elements = tree.xpath(structure[field]["xpath"])
            structure[field]["elements"] = elements
            lengths = len(elements)
        except:
            print(field + " not found.")
        
    #arrays of elements are iterated through and transformed
    for l in range(0, lengths):
        obj = {}
        for field in keys:
            obj[field] = structure[field]["transform"](structure[field]["elements"][l])
        couplings.append(obj)
    
    return couplings

    
url = "https://de.indeed.com/cmp/Getyourguide/jobs"

#this has the name of the field you are interested in, an xpath to find the element on the page, and a function that allows you to grab the data and transform it (see getText())
structure = {
    "jobtitle": {
        "xpath": "//div[@class='cmp-JobListItem-title']",
        "transform": getText,
    },
    "dateposted": {
        "xpath": "//div[@class='cmp-JobListItem-timeTag']",
        "transform": getText,
    }
}

tree = getTree(url)
couplings = getCouplings(tree, structure)
pprint(couplings)

