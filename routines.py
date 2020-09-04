def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

routineA = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "method": "a",
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
        "type": "c",
        "head": "window._initialData=JSON.parse('",
        "tail": "');"
        },
    "structure": {
        "jobtitle": {
            "path": "//div[@class='cmp-JobListItem-title']",
        },
        "dateposted": {
            "path": "//div[@class='cmp-JobListItem-timeTag']",
        }
    }
}