from pprint import pprint
from helpers import getTree
import json
import time
#scrapes elements based off of field selectors
def A(browser, routine):
    tree = getTree(routine["url"])
    structure = routine["structure"]
    data = [] 
    count = None 
    keys = structure.keys()

    for field in keys:
        try:
            elements = tree.xpath(structure[field]["path"])
            structure[field]["elements"] = elements
            length = len(elements)
            if count == None:
                count = length
            else:
                if length != count:
                    print ("error - number of elements differ per item.")
                    return None
        except Exception as e:
            print(e)
            return None

    for l in range(0, count):
        obj = {}
        for field in keys:
            if "transformer" in structure[field].keys():
                obj[field] = structure[field]["transformer"](structure[field]["elements"][l])
            else:
                obj[field] = structure[field]["elements"][l].text 
        data.append(obj)
    
    return data

#scrapes fields through a script in the header
def C(browser, routine):
    tree = getTree(routine["url"])
    head = routine["method"]["head"]
    tail = routine["method"]["tail"]
    keys = routine["structure"].keys()
    stolenScript = {}
    scripts = tree.xpath('//script')
    data = {}
    for script in scripts:
        raw = script.text
        if head in str(raw):
            raw = raw.split(head)[1]
            raw = raw.split(tail)[0]
            encoded = raw.encode('utf-8')
            stolenScript = json.loads(encoded, strict=False)
            break
    for field in keys:
        path = routine["structure"][field]["path"]
        route = stolenScript
        for p in path:
            route = route[p]
        if "transformer" in routine["structure"][field].keys():
            data[field] = routine["structure"][field]["transformer"](route)
        else:
            data[field] = route
    return data 

def B(routine):
    def explore(data, tree, roadmap, depth, root):
        items = roadmap.items()
        for branch in tree:
            if depth == 1:
                root = branch
                data[root] = {}
            fields = {}
            for item in items:
                key = item[0]
                obj = item[1]
                if key == "value":
                    return True
                leaf = branch.find_elements_by_xpath(key)
                valueFound = explore(data, leaf, obj, depth + 1, root)
                if valueFound == True:
                    element = branch.find_elements_by_xpath(key)
                    transformer = obj["transformer"]
                    value = transformer(element[0])
                    fields[obj["value"]] = value
                    if depth == 1:
                        data[root] = {**data[root], **fields}
                    if depth > 1:
                        data[root] = {**data[root], **fields}
        return data
    browser = routine["method"]["browser"]
    browser.get(routine["url"])
    time.sleep(5)  
    tree = browser.find_element_by_xpath("//body")
    roadmap = routine["structure"]
    data = explore({}, [tree], roadmap, 0, None)
    return list(data.values())


    
    
