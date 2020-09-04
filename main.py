from consume import run
from pprint import pprint

def getText(element):
    return element.text

routine = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "structure": {
        "jobtitle": {
            "xpath": "//div[@class='cmp-JobListItem-title']",
        },
        "dateposted": {
            "xpath": "//div[@class='cmp-JobListItem-timeTag']",
            "transformer": getText,
        }
    }
}

result = run(routine)

pprint(result)

