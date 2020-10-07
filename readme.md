# ghettobird

A Python framework/tool designed for web scraping.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install ghettobird
```

## Goals

- reduce scrapers down into a single JSON object, with a few auxilary functions
   - reduce the amount of boilerplate code in scraping projects.
   - make scrapers readable
   - group fragile code together for easy maintenance
   - reduce inconsistancies in error handling
- automate and hasten the development of scrapers
- reduce the need for xpaths

## Usage

```python
from ghettobird import fly

itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            "iterate": "//div[@class='job']",
            "title": ".//h4[@class='title']",
            "description": ".//div[@class='description']",
            "dateposted": ".//div[@data-element-type='date']",
            "salary": "//h3[@id='salary-query']",
        }]
    },
}

fly(itinerary)
```

<!-- ## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/) -->