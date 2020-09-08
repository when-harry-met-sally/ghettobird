Ghettobird Scraping Framework/Tool
-----------------------------
The goal of this project is to:
   - reduce scrapers down into a single JSON object, with a few auxilary functions

By doing this we can:
   - reduce the amount of boilerplate code in scraping projects.
   - make scrapers readable
   - group fragile code together for easy maintenance
   - reduce inconsistancies in error handling

Bonus:
 
   - if the structure of scrapers can be simplified, we can automate the generation
     of scrapers

This tool does not yet include:
   - IP rotation, networking, or security

Why?
   - Unethical, but more importantly, I know nothing about it

---------------------------------------------------------------------------------
The Ghettobird Dictionary/JSON

Reserved keywords: "path", "transformer", "args, "iterate"

This summary will focus on the FLIGHTPATH, which will guide the scraper to our desired data, and provide intructions when it encounters its data

The structure of the FLIGHTPATH is preserved when results are yielded, with the exception of "paths" and "transformer" functions, which will be replaced with our desired values

Sample tranformer function:

def TRANSFORM_get_value(element):
    return element.get("text")

"url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
"flightpath": {
    "header": {
        "path": "//*[@class='page-header']",
        "transformer": TRANSFORM_get_value
    }
}

The result ------------------------->

"flightpath": {
    "job_title": "Jobs in St. Louis, Missouri"
}

--------------------------------------

An element is selected by xpaths and TRANSFORM function generally grabs the data, and/or modifies the data after. 

However, in the absence of a transform function, element.get("text) will always be called. Meaning that a transform function would be necessary for something 
like an input field. But is not generally necessary if you are just grabbing plain text from a DIV, SPAN or P tag.

Similiarly, the "path" field in a dictionary is not always needed.

Example:

"flightpath": {
    "salary_range": {
         "path": "//*[@id='salary-query']",
         "transformer": TRANSFORM_get_text
    },
}

Because the transformer function can be dropped in this situation, and "path" would be the only key within our "id_tech_jobsopen" object, we can actually remove both keys:

"flightpath: {
    "salary_range": "//*[@id='salary-query']",
}

The result ------------------------->

"flightpath": {
    "salary_range":  "Salary Range: 10,000 - 100,000"
}

--------------------------------------

Values that are objects {} or strings, will find only the first element that matches a given xpath. 

Wrapping a dictionary value in an array, will find all results matching the xpath.

"flightpath": {
    "job_titles": ["//*[@class='title']"],
}

The result ------------------------->

"flightpath": {
    "job_titles": ["Senior Software Dev", "Agile Coach", "Software Engineer", "Junior Software Dev", "Ping Pong Player"]
}

-------------------------------------

It is often necessary to couple/group fields.

"flightpath": {
    "job_titles": ["//*[@class='title']"],
    "job_descriptions": ["//*[@class='description']"],
}

This flightpath would return two arrays, but there would be nothing binding a title to its associated description.

To do this, we must use the "iterate" keyword.

Coupling fields: 

"jobs": [{
             "iterate": "//div[@class='job']",
             "title": ".//*[@class='title']",
             "description": ".//*[@class='description']",
         }],

Notice that we have an array of objects. The keyword "iterate" is necessary. As is the period that precedes the xpath. 

Iterate will loop through all divs with the class of "job", and then try to find elements with xpaths of tittle, and description. 

The result ------------------------->

"flightpath": {
    jobs: [{
        "title": "Senior Software Dev",
        "description": "Need a master of React Native, a man or woman with gumption, who can lead a team."
    },
    {
        "title": "Agile Coach",
        "description": "Need a trained agility coach who can combat followers of the waterfall method. Zealotry required."
    },
    ...]
}

(4 more entries would follow)

-------------------------------------






