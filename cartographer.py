
#-----------------------------------------------------------------------------
#
#
# under construction
#
#-----------------------------------------------------------------------------










from helpers import getTree
from pprint import pprint
import copy
# def method(tree, sample):
#     keys = sample.keys()
#     pprint(keys)
#     routine = {}
#     for field in keys:
#         x = '//*[(text() = "{}")]'.format(sample[field])
#         elements = tree.xpath(x)
#         if len(elements) == 0:
#             print("field '{}' not found".format(field))
#             return None
#         element = elements[0]
#         tag = element.tag
#         className = element.get('class')
#         xpath = "//{}[@class='{}']".format(tag, className)
#         routine[field] = {
#             "path": xpath
#         }
#     return routine

def cartograph(desired):
    def explore(des, tree):
        pprint(des)
        goal = copy.deepcopy(des)
        keys = goal.keys()
        for key in keys:
            obj = goal[key]
            typeOfObj = type(obj)
            if typeOfObj == dict:
                continue
            if typeOfObj == list:
                profile = obj[0]
                typeOfSub = type(profile)
                if typeOfSub == str:
                    test = {key: profile}
                    test = explore(test, tree)
                    goal[key] = [test[key]]
                if typeOfSub == dict:
                    expander = None
                    subK = list(profile.keys())
                    subKeys = list(profile.values())
                    fields = {}
                    for s in range(0, len(subKeys)):
                        text = subKeys[s]
                        parent = None
                        if s == 0:
                            expander = findXpath(tree, text)
                            fields[subK[s]] = getUniqueXpath(tree.xpath(expander)[0])
                        else:
                            while True:
                                parent = tree.xpath(expander + "/parent::*")
                                parent = parent[0]
                                parentPath = getUniqueXpath(parent)
                                xpath = "{}/*[contains(text(), '{}')]".format(parentPath, text)
                                pprint(xpath)
                                elements = tree.xpath(xpath)
                                if len(elements) != 0:
                                    path = getUniqueXpath(elements[0])
                                    fields[subK[s]] = path
                                    expander = parentPath
                                    break
                    fields["iterate"] = expander
                    goal[key] = [fields]                        
                continue
            if typeOfObj == str:
                xpath = findXpath(tree, obj)
                goal[key] = xpath
                continue
        return goal
    tree = getTree("http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/")
    result = explore(desired, tree)
    print('-------RESULT-------')
    pprint(result)
    
def findXpath(tree, text):
    x = '//*[contains(text(), "{}")]'.format(text)
    elements = tree.xpath(x)
    element = elements[0]
    xpath = getUniqueXpath(element)
    return xpath

def getUniqueXpath(element):
    tag = element.tag
    className = element.get('class')
    xpath = "//{}[@class='{}']".format(tag, className)
    return xpath


desired = {
    "header": "Jobs in St. Louis, Missouri",
    "titles": ["Senior Software Dev"],
    "jobs": [{
        "title": "Senior Software Dev",
        "description": "Need a master of React Native, a man or woman with gumption, who can lead a team.",
    }]
}


# desired = {
#     "header": "sales jobs",
#     "titles": ["Solar Sales Specialist"],
#     "jobs": [{
#         "title": "Solar Sales Specialist",
#         "description": "Bella Villa, MO",
#     }]
# }

cartograph(desired)

