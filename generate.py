from pprint import pprint
from lxml import html
import json
from helpers import getTree

def methodA(tree, sample):
    keys = sample.keys()
    pprint(keys)
    routine = {}
    for field in keys:
        x = '//*[(text() = "{}")]'.format(sample[field])
        elements = tree.xpath(x)
        if len(elements) == 0:
            print("field '{}' not found".format(field))
            return None
        element = elements[0]
        tag = element.tag
        className = element.get('class')
        xpath = "//{}[@class='{}']".format(tag, className)
        routine[field] = {
            "xpath": xpath
        }
    return routine

# sample = {
#     "url": "https://de.indeed.com/cmp/Getyourguide/jobs", 
#     "fields": {
#         "jobtitle": "Connectivity Operations Team Manager",
#         "location": "Berlin"
#     }
# }

def generateRoutine(sample):
    url = sample["url"]
    tree = getTree(url)
    routine = methodA(tree, sample["fields"])
    return routine


# with open('generated.json', 'w') as outfile:
#     json.dump(structure, outfile)

