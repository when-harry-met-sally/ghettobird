# ghettobird

A Python framework/tool designed for web scraping.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install ghettobird
```

## Goals

The primary goal for this project is to simplify scraping applications into a single dictionary/JSON object (with a few functions sprinkled in).
**This allows us to:**
- Reduce boilerplate code
- Increase code readability
- Group fragile pieces of code for easy maintenance 
- Reduce inconsistancies in error handling
**Overall:**
- Automate and hasten the development of scrapers



## Usage

```python
from ghettobird import fly, iterate

itinerary = {
    "url": "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com",
    "flightpath": {
        "header": "//*[@class='page-header']",
        "jobs": [{
            iterate: "//div[@class='job']",
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