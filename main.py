from ghettobird import run
from generate import generateRoutine
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from pprint import pprint
from seleniumMethods import A, B, C

def getText(element):
    return element.text
def getHref(element):
    return element.get("href")

 #scrapes an indeed company
roadmapA = {
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
roadmapC = {
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

#scrapes indeed just like roadmapA
roadmapB = {
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
            },
            ".//div[@class='cmp-JobListItem-tags']": {
                ".//div[@class='cmp-JobListItem-timeTag']": {
                    "value": "time",
                    "transformer": getText
                }
            }
        }
     }
}

chromedriver_location = 'c:/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromedriver_location)

roadmapBselenium = {
    "url": "https://de.indeed.com/cmp/Hellofresh/jobs?jk=22c38db700e6b578&start=0&clearPrefilter=1",
    "method": {
        "type": B,
        "browser": browser,
        "sleep": 2
    },
    "structure": {
        "//div[@class='cmp-JobDetail']": {
            ".//div[@class='cmp-JobDetailTitle']": {
                "value": "jobtitle",
                "transformer": getText
            },
            ".//div[@class='cmp-JobDetailDescription-description']": {
                "value": "jobdesc",
                "transformer": getText
            },
        }
     }
}

result = run(roadmapBselenium)
pprint(result)


