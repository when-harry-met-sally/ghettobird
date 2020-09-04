def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

modelA = {
    "jobtitle": {
        "xpath": "//div[@class='cmp-JobListItem-title']",
    },
    "dateposted": {
        "xpath": "//div[@class='cmp-JobListItem-timeTag']",
        "transform": getText,
    }
}