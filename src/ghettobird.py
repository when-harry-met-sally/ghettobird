from helpers import getTree
import copy
import json
import time
from pprint import pprint
#---------------RESERVED KEYWORDS------------------
iterate = "GB_iterate"
transformer = "GB_transformer"
#---------------DEFAULT OPTIONS--------------------
def default_alert():
    print('\007')
    input("--Interrupt Selector Detected: Press Any Key to Continue--")
#---------------FLIGHT OPTIONS---------------------
flight_options = {
    "interrupt_selectors": [], #takes an array of string xpath selectors
    "interrupt_retries": 3, #amount of retries taken before giving up and return empty results object
    "interrupt_alert": default_alert, #alert function triggeredw hen an interrupt selector is found
    "browser": None, #selenium browser. None-type will cause the basic_tree method function
    "pause": 3, #time in seconds that sleep after a get request. selenium only
}
#---------------TRANSFORM FUNCTIONS----------------
def TRANSFORM_getText(element):
    text = element.text.strip()
    return text
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
#---------------SELENIUM METHOD--------------------
def selenium_method(flight):                     #-
    opts = flight["options"]
    browser = opts["browser"]
    pause = opts["pause"]
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
                        element = tree.find_element_by_xpath(obj["path"])
                    except Exception as e: 
                        log.append("{} | {} element not found.".format(e, key))
                        flightpathCopy[key] = ""
                        continue
                    try:
                        for inner in innerKeys:
                            if inner == transformer:
                                flightpathCopy[key] = obj[transformer](element)
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
                    iterater = "//html"
                    branch = None
                    if iterate in profile.keys():
                        iterater = profile.pop(iterate)
                    branches = tree.find_elements_by_xpath(iterater)
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
                        elements = tree.find_elements_by_xpath(profile)
                    except Exception as e: 
                        log.append("{} | {} is an invalid xpath".format(e, key))
                        leaves = []
                        continue
                    for element in elements:
                        leaves.append(TRANSFORM_getText(element))
                flightpathCopy[key] = leaves
            if typeOfObj == str:
                try:
                    element = tree.find_element_by_xpath(obj)
                    flightpathCopy[key] = TRANSFORM_getText(element)
                except Exception as e:
                    log.append("{} | {} not found".format(e, key))
                    flightpathCopy[key] = ""
                    continue

        return flightpathCopy
    retries = opts["interrupt_retries"]
    tree = None
    while retries > -1:
        browser.get(flight["url"])
        time.sleep(pause)
        tree = browser.find_element_by_xpath("//html")
        interruptions = interrupt_check(tree, opts["interrupt_selectors"])
        if interruptions is True:
            retries = retries - 1
            time.sleep(pause)
            opts["interrupt_alert"]()
            print("--Retries remaining: {}".format(str(retries)))
            if retries == 0:
                return {}
        else:
            break
    results = explore(tree, flight["flightpath"], flight["log"])
    return results                              #-
#---------------NON-SELENIUM METHOD----------------
def tree_method(flight):
    opts = flight["options"]
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
                            if inner == transformer:
                                flightpathCopy[key] = obj[transformer](element)
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
                    iterater = "//html"
                    branch = None
                    if iterate in profile.keys():
                        iterater = profile.pop(iterate)
                    branches = tree.xpath(iterater)
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
    retries = opts["interrupt_retries"]
    tree = None
    while retries > -1:
        tree = getTree(flight["url"])
        interruptions = interrupt_check(tree, opts["interrupt_selectors"])
        if interruptions is True:
            retries = retries - 1
            opts["interrupt_alert"]()
            print("--Retries remaining: {}".format(str(retries)))
            if retries == 0:
                return {}
        else:
            break
    results = explore(tree, flight["flightpath"], flight["log"])
    return results

def interrupt_check(tree, selectors):
    for selector in selectors:
        if len(tree.xpath(selector)) > 0:
            print(selector.format(" detected"))
            return True
    return False

def handleOptions(routine):
    if "options" in list(routine.keys()):
        opts = routine["options"]
        for option in list(opts.keys()):
            flight_options[option] = opts[option] 
    routine["options"] = flight_options
    
def fly(routine):
    routine["log"] = []
    handleOptions(routine)
    opts = routine["options"]
    if opts["browser"] is None:
        routine["results"] = tree_method(routine)
    else:
        routine["results"] = selenium_method(routine)
    return routine
