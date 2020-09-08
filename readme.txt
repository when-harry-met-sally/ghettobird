Ghettobird Scraping Framework
-----------------------------
The goal of this framework is to:
   - reduce the amount of boilerplate code in scraping projects.
     this includes try/catch blocks and reoccuring patterns
   - make scrapers readable
   - group fragile code together for easy maintenance

I hope to do this by:

   - reducing the scraper to a dictionary of xpaths, and auxilary functions

And as a bonus,
 
   - if the structure of scrapers can be simplified, develope a method for those
     unfamiliar with xpaths to generate the generate the dictionary structure 
     with a little user input

I don't know much about IP rotation, networking, or security. That will come later...

---------------------------------------------------------------------------------
Ghettobird dictionary structure:

Reserved keywords: "path, transformer, args, scope"

This summary will focus on the ROADMAP, which will guide the scraper to our desired data

The structure of the roadmap will be preserved with the exception of paths and transformer functions, which will be replaced with our desired values

def TRANSFORM_get_value(element):
    return element.get("value")

"url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
"roadmap": {
    "job_title": {
        "path": "//input[@id='what']"
        "transformer": TRANSFORM_get_value
    }
}

Assuming nothing goes wrong, the result will be ----------->

"roadmap": {
    "job_title": "Douglas Parfümerie"
}

An element is selected with xpathsm and TRANSFORM function will generally grab the data, and often times transform it. We are selecting a input in this case, so it is 
necessary to grab "value".

A plain old div would require:

def TRANSFORM_get_text(element):
    return element.get("text)

However, in the absence of a transform function, element.get("text) will always be called. Meaning that a transform function would be necessary for an input field,
but not necessary if you are just grabbing text from a div, span or p tag.

Similiarly, the "path" field in a dictionary is not always needed.

Example:

"roadmap": {
    "id_tech_jobsopen": {
         "path": "//div[@id='searchCountPages']",
         "transformer": TRANSFORM_get_text
    },
}

Because the transformer function can be dropped in this situation, and "path" would be the only key within our "id_tech_jobsopen" object, we can actually remove both keys:

"roadmap: {
    "id_tech_jobsopen": "//div[@id='searchCountPages']"
}

Combined --->

"roadmap": {
    "id_tech_jobsopen": "//div[@id='searchCountPages']",
    "job_title": {
        "path": "//input[@id='what']"
        "transformer": TRANSFORM_get_value
    }
}


Both of these fields will only return the first element that matches the give xpath.
A field must be wrapped in an array to return multiple values.

Example:

"roadmap": {
    "id_tech_jobsopen": ["//div[@id='searchCountPages']"],
    "job_title": [{
        "path": "//input[@id='what']"
        "transformer": TRANSFORM_get_value
    }]
}

This would return an array for both entries.

Coupling fields: 

"jobs": [{
             "scope": "//div[@data-tn-component='organicJob']",
             "title": {
                "path": ".//a[@data-tn-element='jobTitle']",
             },
            "link": {
                "path": ".//a[@data-tn-element='jobTitle']",
                "transformer": getHref
             },
             "dateposted": {
                "path": ".//span[@class='date ']"
             },
            "location": {
                "path": ".//span[@class='location accessible-contrast-color-location']",
             }
         }],

Notice this is a dictionary within an array. If we removed the brackets (the list), each field "title", "link", "datepoted" and "location", would all return one value.
We would be left with a dictionary, with these 4 fields, all describing the first job out of many.

The most important field here is "scope", it's a reserved keyword. It narrows the cope of the xpaths that follow. 

Assume there are 10 elements that contain details about 10 jobs. The scope xpath ensures we iterate through each container, and the the four fields from within the container.
This way our result ends with a list of job objects with unique details...

[{
    "title": Software dev,
    "link": www.google.com,
    "datepoted": yesterday,
    "location": STL,
    {
    "title": Agile coach,
    "link": www.google.com,
    "datepoted": today,
    "location": antarctica
    }, ...
}]

(NOTE: I think the scope attribute is a bit inconsistant, could use a change)

-----------------------------------------------------------------------------------------
My plan for the roadmap generator is as follows:

A user enters in a desired output given a URL: 

That could be:

[
    "company": "GOOGLE",
    {
    "title": Software dev,
    "link": www.google.com,
    "datepoted": yesterday,
    "location": STL,
}.{
    "title": Agile coach,
    "link": www.google.com,
    "datepoted": today,
    "location": antarctica
    }, ...
}]


And we reverse engineer our way to a roadmap structure that can be applied to all URLS following that sturcture. Array notation or dictionary notation is important here.

For single values that we except to occur once on the page. 

We use an xpath that searches for matching text, we then analyze css selectors and id, to find out if there is a unique identifier that only returns that element.

For object arrays, it is a bit tricker.

We start from the first value of the first entry, we go to the parent node to parent node until we have a node that is ap arent of all fields within the dictionary, but not
including the second item's members. We then grab css selectors and or id. 

-----SELENIUM ISSUE----
The function used needs to accomodate fo rselenium and regular xpaths.





