from pprint import pprint
from lxml import html
import requests
import json


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


#given the object "structure", those who are unfamiliar with xpath can have a dictionary built for them. This obviosly needs to be refined, but by having a user input
#information on the first item, IE, jobtitle and dataposted, we can build the blueprint to a method of scraping

#right now, a transformative function can't really be generated. but we could throw in a "desired" field on the structure object, 
#actual = "posted 7 days ago" -----> desired = "7 days"
#if the words are not in the desired replace(""posted, ""), replace(ago, "")
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

#for the transformative function, we also add the words we hope to replace in the jason, they are looped through and removed
