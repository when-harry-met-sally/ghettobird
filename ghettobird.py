from helpers import getTree
import copy
import json

#---------------TRANSFORM FUNCTIONS----------------
def TRANSFORM_getText(element):
    return element.text
def TRANSFORM_getHref(element):
    return element.get("href")
def TRANSFORM_getValue(element):
    return element.get("value")
def TRANSFORM_parseJSONfromScript(element, args):
    data = {}
    keys = args.keys()
    raw = element.text
    if "head" in args and "tail" in args:
        head = args["head"]
        tail = args["tail"]
        raw = raw.replace(head, "")
        raw = raw.replace(tail, "")
        args.pop("head")
        args.pop("tail")
    try:
        raw = raw.encode('utf-8')
        raw = json.loads(raw, strict=False)
    except Exception as e:
        raw = raw.encode('ascii', 'ignore').decode('unicode_escape')
        raw = json.loads(raw, strict=False)
        print("error while encoding json")
        print(e)
    for field in keys:
        path = args[field]
        route = raw
        for p in path:
            if p in route.keys():
                route = route[p]
            else:
                print("{} not found".format(p))
                route = ""
                break
        data[field] = route
    return data
#---------------NON-SELENIUM METHOD----------------
def basic_method(flight):
    def explore(tree, flightpath, log):
        flightpathCopy = copy.deepcopy(flightpath)
        keys = flightpathCopy.keys()
        for key in keys:
            obj = flightpathCopy[key]
            typeOfObj = type(obj)
            if typeOfObj == dict:
                innerKeys = obj.keys()
                if "path" in innerKeys:
                    element = None
                    try:
                        element = tree.xpath(obj["path"])[0]
                        
                    except Exception as e: 
                        log.append("{} | {} element not found.".format(e, key))
                        flightpathCopy[key] = ""
                        continue
                    try:
                        for inner in innerKeys:
                            if inner == "transformer":
                                flightpathCopy[key] = obj["transformer"](element)
                            elif callable(inner):
                                flightpathCopy[key] = inner(element, obj[inner])
                            else:
                                flightpathCopy[key] = TRANSFORM_getText(element)
                    except Exception as e: 
                        log.append("{} | {} transformer function failed.".format(e, key))
                        print(e)
                else:
                    flightpathCopy[key] = explore(tree, obj, log)
            if typeOfObj == list:
                profile = {}
                try:
                    profile = obj[0]
                except Exception as e: 
                    log.append("{} | {} list is empty.".format(e, key))
                    flightpathCopy[key] = []
                    continue
                typeOfProfile = type(profile)
                if typeOfProfile == dict:
                    iterate = "//html"
                    branch = None
                    if "iterate" in profile.keys():
                        iterate = profile.pop("iterate")
                    branches = tree.xpath(iterate)
                    if len(branches) == 0:
                        log.append("{} container element for list not found".format(key))
                        flightpathCopy[key] = []
                        continue
                    leaves = []
                    for branch in branches:
                        leaves.append(explore(branch, profile, log))
                    flightpathCopy[key] = leaves
                    continue
                leaves = []
                if typeOfProfile == str:
                    try:
                        elements = tree.xpath(profile)
                    except Exception as e: 
                        log.append("{} | {} is an invalid xpath".format(e, key))
                        leaves = []
                        continue
                    for element in elements:
                        leaves.append(TRANSFORM_getText(element))
                flightpathCopy[key] = leaves
            if typeOfObj == str:
                try:
                    element = tree.xpath(obj)[0]
                    flightpathCopy[key] = TRANSFORM_getText(element)
                except Exception as e:
                    log.append("{} | {} not found".format(e, key))
                    flightpathCopy[key] = ""
                    continue

        return flightpathCopy

    tree = getTree(flight["url"])
    results = explore(tree, flight["flightpath"], flight["log"])
    return results

def fly(routine):
    routine["log"] = []
    routine["results"] = basic_method(routine)
    return routine
