from html.parser import HTMLParser
from urllib import parse


# so in this class what I am doing is that: I will create
# a link finder object, and we are going to feed it in
# html of some random page (homepage) for example
# so once it get all the links right here we can go
# ahead and call the page_links function, and then we
# get all the links that we can use in our program save
# them to a file and do whatever we want

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attribute, value) in attrs:
                if attribute == 'href':
                    url = parse.urljoin(self.base_url, value)
                    self.links.add(url)

    def page_links(self):
        return self.links

    def error(self, message):
        pass
