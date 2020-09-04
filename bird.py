from pprint import pprint
from lxml import html
import requests
from datetime import datetime
import json
#idea one
#library that assists in scraping, does try catch shit for you, iterates for you

#idea two
#library that finds convenient xpath for you
#arg1 = item in list you are trying to scrape, arg2 = item in list you are trying to scrape, num of items 
log = []
def errorLog(source, message):
    now = datetime.now() 
    time = now.strftime("%H:%M:%S, %m/%d/%Y")
    log.append([time, source, message])
    print(time + " | " + source + " | " + message)

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
def getHref(element):
    return element.get("href")
#----------------------

def methodA(tree, structure):
    couplings = [] 
    count = None #the amount of entries on the page.
    keys = structure.keys() #fields: jobtitle, dateposted

    #grabs an array of elements for each field in the structure object.
    #jobtitle is given an array of all jobtitle elements
    #dateposted is given an array fo all datepoted elements
    for field in keys:
        try:
            elements = tree.xpath(structure[field]["xpath"])
            structure[field]["elements"] = elements
            length = len(elements)
            if count == None:
                count = length
            else:
                if length != count:
                    print ("error - number of elements differ per item.")
        except:
            errorLog("getCoupling()", "error - " + field + " not found.") #do this shit tomorrow
        
    #arrays of elements are iterated through and transformed
    for l in range(0, count):
        obj = {}
        for field in keys:
            if "transform" in structure[field].keys():
                obj[field] = structure[field]["transform"](structure[field]["elements"][l])
            else:
                obj[field] = structure[field]["elements"][l].text #a lack of a transformative function simply takes text
        couplings.append(obj)
    
    return couplings


url = "https://de.indeed.com/cmp/Getyourguide/jobs"

#this has the name of the field you are interested in, an xpath to find the element on the page, and a function that allows you to grab the data and transform it (see getText())
structure = {}
with open('generated.json') as f:
  structure = json.load(f)


tree = getTree(url)
data = methodA(tree, structure)
pprint(data)
