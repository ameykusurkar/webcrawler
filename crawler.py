import urllib2
from HTMLParser import HTMLParser

class CrawlParser(HTMLParser):
  href_links = []

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      self.count += 1
      self.store_href_link(attrs)

  def store_href_link(self, attrs):
    for (attr, value) in attrs:
      if attr == "href":
        self.href_links.append(value)

  def get_href_links(self):
    return self.href_links

url = "http://www.google.co.uk"
parser = CrawlParser()
content = urllib2.urlopen(url).read()
parser.feed(content)
links = parser.get_href_links()
print(len(links))


