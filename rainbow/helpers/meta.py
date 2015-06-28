import json, urllib.request
from html.parser import HTMLParser

def get_website(event):
    query = event.title.replace(' ', '+')
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=%s" % query
    result = urllib.request.urlopen(url).read()
    json_data = json.loads(result.decode("utf-8"))
    return json_data['responseData']['results'][0]['unescapedUrl']

def get_description(event):
    parser = GetDescriptionHTMLParser()
    parser.feed(urllib.request.urlopen(get_website(event)).read().decode("utf-8"))
    return parser.description

class GetDescriptionHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.description = ""
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            content = ""
            for (k, v) in attrs:
                if k == 'content':
                    content = v
                    break
            for (k, v) in attrs:
                if k == 'name' and v == 'description':
                    self.description = content
                    break

get_description(E())
