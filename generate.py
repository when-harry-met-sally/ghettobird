from pprint import pprint
from lxml import html
import requests
import json
from helpers import getTree

def structureGenerator(tree, sample):
    keys = sample.keys()
    diagnosis = {}
    for field in keys:
        element = tree.xpath('//*[contains(text(),"{}")]'.format(sample[field]))[0]
        tag = element.tag
        className = element.get('class')
        xpath = "//{}[@class='{}']".format(tag, className)
        diagnosis[field] = {
            "xpath": xpath
        }
    return diagnosis

url = "https://de.indeed.com/cmp/Getyourguide/jobs"

sample = {
        "jobtitle": "Senior Backend Engineer, Data Products",
        "dataposted": "vor 6 Tagen"
    }

tree = getTree(url)
structure = structureGenerator(tree, sample)

pprint(structure)

with open('generated.json', 'w') as outfile:
    json.dump(structure, outfile)

