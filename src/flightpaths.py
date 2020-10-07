#---------------FILE OVERVIEW----------------------
#CONTAINS SAMPLE FLIGHTPATHS 
#--------------------------------------------------    


#Paths that are arrays are for JSON objects, string paths are for xpaths

#where a JS object/JSON is within a script, no transforamtion needed
routine = {
    "url": "https://www.glassdoor.com/Overview/Working-at-UniGroup-EI_IE3422.11,19.htm",
    "flightpath": {
        "jobs": {
            "path": "//script[@type='application/ld+json']",
            TRANSFORM_parseJSONfromScript: {
                "rating": ["ratingValue"]
            }
        }
    },
}

#where a JS object/JSON is within a script, but needs to be modified to be loaded into a JSON
#head, tail need to be trimmed from the script text. 
#all other fields (id_company, id_lessText) will be returned with values
routine = {
    "url": "https://de.indeed.com/cmp/Getyourguide", #model URL
    "flightpath": {
        "bio": {
            "path": "//script[contains(text(), 'window._initialData=JSON.parse(')]",
            TRANSFORM_parseJSONfromScript: {
                "head": "window._initialData=JSON.parse('",
                "tail": "');",
                "id_company": ["topLocationsAndJobsStory", "companyName"],
                "id_lessText": ["aboutStory", "aboutDescription", "lessText"]
            },
        }
    }
}

#typical routine where we grab non-script elements, nothing fancy
routine = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            "iterate": "//div[@class='job']",
            "title": ".//h4[@class='title']",
            "description": ".//h4[@class='description']",
            "dateposted": ".//div[@data-element-type='date']",
            "salary": "//h3[@id='salary-query']",
        }]
    },
}
