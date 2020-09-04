def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

routineA = {
    "url": "https://de.indeed.com/cmp/Getyourguide/jobs",
    "structure": {
        "jobtitle": {
            "xpath": "//div[@class='cmp-JobListItem-title']",
            "transformer": getText, #optional
        },
        "dateposted": {
            "xpath": "//div[@class='cmp-JobListItem-timeTag']",
            "transformer": getText #optional,
        }
    }
}
