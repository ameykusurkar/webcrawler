from urllib2 import urlopen, URLError
from HTMLParser import HTMLParser
from urlparse import urljoin

# Given a URL, parser finds all the links and static assets on the page
class CrawlParser(HTMLParser):

  def __init__(self, base_url):
    if base_url[-1] != '/':
      base_url += '/'
    self.base_url = base_url
    self.href_links = []
    self.assets = []
    HTMLParser.__init__(self)

  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      self.add_attr('href', attrs, self.href_links)
    if tag == 'link':
      self.add_attr('stylesheet', attrs, self.assets)
    if tag == 'script' or tag == 'img':
      self.add_attr('src', attrs, self.assets)

  def add_attr(self, attr_name, attrs, dest):
    data = self.get_attr_value(attr_name, attrs)
    if data:
      full_url = urljoin(self.base_url, data)
      dest.append(full_url)

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

