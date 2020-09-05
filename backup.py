def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

#scrapes elements based off of field selectors
def A(routine):
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
def C(routine):
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
    
 #scrapes an indeed company
routine1 = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "method": {
        "type": A,
    },
    "structure": {
        "jobtitle": {
            "path": "//div[@class='cmp-JobListItem-title']",
            "transformer": getText, #optional
        },
        "dateposted": {
            "path": "//div[@class='cmp-JobListItem-timeTag']",
            "transformer": getText #optional,
        }
    }
}

#scrapes a glassdoor company
routineC = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "method": {
        "type": C,
        "head": "window._initialData=JSON.parse('",
        "tail": "');"
        },
    "structure": {
        "jobtitle": {
            "path": ["route", "pathname"]
        },
    }
}