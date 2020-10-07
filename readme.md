# ghettobird

A Python framework/tool designed for web scraping.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

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
Usage examples feature this [website](http://ghettobird.sample.s3-website.us-east-2.amazonaws.com/ "Sample Website"). It is a static HTML page, but a JS-heavy sample will be added soon.

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
**Example Two**: Grabbing a list

If we wanted to grab every single job title from our sample page, the following flightpath would be appropriate. Notice the brackets that surround our xpath. This allows us to return multiple values from elements.

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
            'Ping Pong Player']}
```
**Example Three**: Transformer functions

By default, elements that are found with a given xpath have their text values returned unless specified otherwise. However, if we need to perform some sort of transformation on the element or get an HREF rather than text, "transformer" functions will be necessary. 
```python
from ghettobird import fly, transformer
```
```python
itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "links": {
["//h4[@class='title']"],
    },
}
```
We would be returned with dictionary that follows the blueprint we laid out, but with the data being populated with:

```python
{'titles': ['Senior Software Dev',
            'Agile Coach',
            'Software Engineer',
            'Junior Software Dev',
            'Ping Pong Player']}
```
```python
{'header': 'Jobs in St. Louis, Missouri',
 'jobs': [{'dateposted': '(Date Posted: 9/9/2020)',
           'description': 'Need a master of React Native, a man or woman with '
                          'gumption, who can lead a team.',
           'salary': 'Salary Range: 10,000 - 100,000',
           'title': 'Senior Software Dev'},
          {'dateposted': '(Date Posted: 9/8/2020)',
           'description': 'Need a trained agility coach who can combat '
                          'followers of the waterfall method. Zealotry '
                          'required.',
           'salary': 'Salary Range: 10,000 - 100,000',
           'title': 'Agile Coach'},
          {'dateposted': '(Date Posted: 9/8/2020)',
           'description': 'Need a remote Java whiz who can do build a bowling '
                          'scoring app.',
           'salary': 'Salary Range: 10,000 - 100,000',
           'title': 'Software Engineer'},
          {'dateposted': '(Date Posted: 9/8/2020)',
           'description': 'Need a spry, young developer who can juggle.',
           'salary': 'Salary Range: 10,000 - 100,000',
           'title': 'Junior Software Dev'},
          {'dateposted': '(Date Posted: 9/9/2020)',
           'description': 'Need an athetlic ping pong player.',
           'salary': 'Salary Range: 10,000 - 100,000',
           'title': 'Ping Pong Player'}]}

```

