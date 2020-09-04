from consume import run
from generate import generateRoutine
from pprint import pprint
from methods import A, C

def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

routine1 = { #scrapes an indeed company for job titles and days posted
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

#sample for indeed


result = run(routine1)
pprint(result)

# pprint(result)

