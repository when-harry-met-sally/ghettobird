from lxml import html
import requests

def getTree(URL):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        'Accept-Language': 'en-gb',
        'Accept-Encoding': 'br, gzip, deflate',
        'Accept': 'test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    try:
        r = requests.get(URL, headers=headers, timeout=10)
        tree = html.fromstring(r.content.decode("utf-8", "replace"))
        return tree
    except Exception as e:
        print(e)
        return None

def scrape():
    url = "http://ghettobird.sample.s3-website.us-east-2.amazonaws.com"
    tree = getTree(url)
    data = {
        "header": tree.xpath("//*[@class='page-header']")[0].text,
        "jobs": []
    }
    jobs = []
    jobContainers = tree.xpath("//div[@class='job']")
    for container in jobContainers:
        job = {
            "title": container.xpath(".//h4[@class='title']")[0].text,
            "description": container.xpath(".//div[@class='description']")[0].text,
            "dateposted": container.xpath(".//div[@data-element-type='date']")[0].text,
            "salary": container.xpath("//h3[@id='salary-query']")[0].text
        }
        data["jobs"].append(job)
    print(data)
scrape()

#this script does not do error handling or logging, both included with ghettobird
