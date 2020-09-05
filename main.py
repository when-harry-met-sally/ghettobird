from ghettobird import run
from generate import generateRoutine
from pprint import pprint
from methods import A, B, C

def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

 #scrapes an indeed company
routineA = {
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

routineB = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "method": {
        "type": B,
    },
    "structure": {
        "//a[@class='cmp-JobListItem-anchor']": {
            ".//div[@class='cmp-JobListItem-title']": {
                "value": "jobtitle",
                "transformer": getText
            },
            ".//div[@class='cmp-JobListItem-subtitle']": {
                "value": "location",
                "transformer": getText
            }
        }
     }
}

result = run(routineB)
pprint(result)


