
# ghettobird

A Python framework/tool designed for web scraping.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ghettobird.

```bash
pip install ghettobird
```

## Goals

The primary goal of this project is to simplify scraping applications into a single dictionary/JSON object (with a few auxilary functions sprinkled in).

**This allows us to:**
- Reduce boilerplate code
- Increase code readability
- Group fragile pieces of code for easy maintenance
- Reduce inconsistancies in error handling

## Usage
Example cases feature this [website](http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/ "Sample Website"). It is static HTML and the data is retreived with a GET request. However, Ghettobird also allows for the scraping of Javascript-heavy pages, where data is not transmitted through a GET request, and is instead loaded with JS. For complex websites like Facebook or sites where data is revealed after interacting with the page itself (through mouse clicks, logins, and the like), we can simply add an "options" key to the itinerary object seen below.
```python
from ghettobird import fly

itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
    },
    "options" : {
	    "browser": browser #a Selenium browser object goes here
	}
}

results = fly(itinerary)["results"]
```
Using the Selenium method of scraping will require you to install Selenium and a webdriver. Instructions can be found [here](https://selenium-python.readthedocs.io/).

For now, we will work with a simple website. Let's import Ghettobird.
```python
from ghettobird import fly
```

**Example One**: Grabbing a single element

If we wanted to grab a page header from our sample page and we expect only one element to be returned, we could use the following "flightpath":

```python
itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
    },
}
```
We would be returned with dictionary that follows the blueprint we laid out, but with the data being populated with:

```python
{'header': 'Jobs in St. Louis, Missouri'}
```
The key "header" could be named anything we want, and it's corrosponding value is an xpath that serves as directions to our desired data. 
 
**Example Two**: Grabbing a list

If we wanted to grab every single job title from our sample page, the following flightpath would be appropriate. Notice the square brackets that surround our xpath. This allows us to return multiple values from elements.

```python
itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "titles": ["//h4[@class='title']"],
    },
}
```
The result:
```python
{'titles': ['Senior Software Dev',
            'Agile Coach',
            'Software Engineer',
            'Junior Software Dev',
            'Ping Pong Player']
 }
```
**Example Three**: Iterating through container elements 

Grabbing the titles of job positions is useful, but let's say we wanted to grab other information about each job object on the page. Let's try to get a title and a description for each job.

We could technically write the following code:
```python
itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "titles": ["//h4[@class='title']"],
        "description": [".//div[@class='description']"]
    }
}
```
This would return two lists, one with our job titles, and one with our job descriptions. This gets the job done, but if we wanted an array of job objects that had the fields of title and description, we would need to transform our data slightly. We are also fortunate that there are 5 titles and 5 descriptions on this page, so this transformation woud be pretty simple. If however, we had 5 titles and 4 descriptions, this would be trickier... How would we know which description goes with a given job title?

What we can do is use the keyword "@iterate". If we can find an HTML element that contains our title and description for our job, we can easily form an array of job objects without writing much code. We will just need an additional xpath.
```python
itinerary = {
   "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
	"flightpath": {
		"jobs": [{
			"@iterate": "//div[@class='job']",
			"title": "//h4[@class='title']",
			"description": ".//div[@class='description']"
		}]
	}
}
```
This would return us 
```python
{
"jobs": [{
		"description": "Need a master of React Native, a man or woman with gumption, who can lead a team.",
		"title": "Senior Software Dev"
		},
		{
		"description": "Need a trained agility coach who can combat followers of the waterfall method. Zealotry required.",
		"title": "Senior Software Dev"
		},
		{
		"description": "Need a remote Java whiz who can do build a bowling scoring app.",
		"title": "Senior Software Dev"
		},
		{
		"description": "Need a spry, young developer who can juggle.",
		"title": "Senior Software Dev"
		},
		{
		"description": "Need an athetlic ping pong player.",
		"title": "Senior Software Dev"
		}]
}
```
**Example Four**: Transfomer functions

So far, all of our example cases have interacted with our desired HTML in the same way: they have grabbed text. However, when scraping it is not unusual to grab href's and other attributes. For cases such as these, transformer functions are necessary. 

They **look** like this:
```python
def TRANSFORM_getHref(element):
	return element.get("href")
```
They are **used** like this:
```python
itinerary = {
	"url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
	"flightpath": {
		"linksOnPage": [{
			"@path": "//a",
			"@transformer": TRANSFORM_getHref
		}]
	},
}
```
The function is passed in with the "@transformer" key and the xpath value is passed in as the "@path" key. Transfomer functions take an argument (element) which is the HTML element that is found with the @path. The value that is returned from the function will populate the field. 


