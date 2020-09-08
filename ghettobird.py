from lxml import html
import requests
import copy

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
    except Exception as e:
        print(e)
        return None

def getText(element):
    return element.text
def getHref(element):
    return element.get("href")
def getValue(element):
    return element.get("value")

def master_method(flight):
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
                        if "transformer" in innerKeys:
                            flightpathCopy[key] = obj["transformer"](element)
                        else:
                            flightpathCopy[key] = getText(element)
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
                        leaves.append(getText(element))
                flightpathCopy[key] = leaves
            if typeOfObj == str:
                try:
                    element = tree.xpath(obj)[0]
                    flightpathCopy[key] = getText(element)
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
    routine["results"] = master_method(routine)
    return routine
