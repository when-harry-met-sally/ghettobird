from pprint import pprint
from datetime import datetime
import json
from helpers import getTree

log = []
def errorLog(source, message):
    now = datetime.now() 
    time = now.strftime("%H:%M:%S, %m/%d/%Y")
    log.append([time, source, message])
    print(time + " | " + source + " | " + message)

def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

def methodA(tree, structure):
    couplings = [] 
    count = None 
    keys = structure.keys()

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
                    return None
        except:
            errorLog("getCoupling()", "error - " + field + " not found.") 
            return None

    for l in range(0, count):
        obj = {}
        for field in keys:
            if "transformer" in structure[field].keys():
                obj[field] = structure[field]["transformer"](structure[field]["elements"][l])
            else:
                obj[field] = structure[field]["elements"][l].text 
        couplings.append(obj)
    
    return couplings

def run(routine):
    tree = getTree(routine["url"])
    print(tree)
    structure = routine["structure"]
    result = methodA(tree, structure)
    return result
