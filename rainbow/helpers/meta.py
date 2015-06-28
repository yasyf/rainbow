import requests, urllib.parse
from html.parser import HTMLParser
from rainbow.helpers.mongo import googlecache

def get_url(event):
    query = urllib.parse.quote_plus(event.title)
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={}".format(query)
    response = requests.get(url).json()
    return response['responseData']['results'][0]['unescapedUrl']

def get_url_and_description(event):
    cached = googlecache.find_one({'title': event.title})
    if cached:
        return cached['url'], cached['description']
    parser = GetDescriptionHTMLParser()
    url = get_url(event)
    parser.feed(requests.get(url).text)
    googlecache.insert({'title': event.title, 'url': url, 'description': parser.description})
    return url, parser.description

class GetDescriptionHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = None

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            content = None
            for (k, v) in attrs:
                if k == 'content':
                    content = v
                    break
            if content:
                for (k, v) in attrs:
                    if k == 'name' and v == 'description':
                        self.description = content
                        break
