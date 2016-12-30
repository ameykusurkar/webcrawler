from urllib2 import urlopen, URLError
from HTMLParser import HTMLParser
from urlparse import urljoin

# Given a URL, parser finds all the links and static assets on the page
class CrawlParser(HTMLParser):

  def __init__(self, base_url):
    self.base_url = base_url
    self.href_links = []
    self.assets = []
    HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      link = self.get_attr_value('href', attrs)
      if link:
        full_url = urljoin(base_url, link)
        self.href_links.append(full_url)
    if tag == 'link':
      stylesheet = self.get_attr_value('stylesheet', attrs)
      if stylesheet:
        full_url = urljoin(base_url, stylesheet)
        self.assets.append(full_url)
    if tag == 'script':
      script = self.get_attr_value('src', attrs)
      if script:
        full_url = urljoin(base_url, script)
        self.assets.append(full_url)
    if tag == 'img':
      image = self.get_attr_value('src', attrs)
      if image:
        full_url = urljoin(base_url, image)
        self.assets.append(full_url)

  def get_attr_value(self, target_attr, attrs):
    for attr, value in attrs:
      if attr == target_attr:
        return value
    return None

  def crawl(self, url):
    try:
      content = urlopen(url).read()
      self.feed(content)
      return self.href_links, self.assets
    except URLError:
      return []
    except ValueError:
      raise

##### SCRIPT #####

base_url = "http://gocardless.com"
parser = CrawlParser(base_url)
links, assets = [], []
try:
  links, assets = parser.crawl(base_url)
except ValueError:
  print("Invalid URL.")
    
for l in links:
  print(l)
print("{} link(s) found.".format(len(links)))
for a in assets:
  print(a)
print("{} assets(s) found.".format(len(assets)))

