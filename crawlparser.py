from urllib2 import urlopen, URLError
from HTMLParser import HTMLParser, HTMLParseError
from urlparse import urljoin

# Given a URL, parser finds all the links and static assets on the page
# Only the method CrawlParser.crawl(url) is called externally
# Other methods are used interally to parse and build data
class CrawlParser(HTMLParser):

  def __init__(self, base_url):
    # base_url needs to end with '/' for urljoin
    # used for converting relative paths into full urls
    if base_url[-1] != '/':
      base_url += '/'
    self.base_url = base_url
    self.href_links = []
    self.assets = []
    HTMLParser.__init__(self)

  # Extracts links and assets as it encounters relevant tags
  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      self.add_attr('href', attrs, self.href_links)
    if tag == 'link':
      # Only add to assets is link is a css stylesheet
      if self.get_attr_value('rel', attrs) == 'stylesheet':
        self.add_attr('href', attrs, self.assets)
    if tag == 'script' or tag == 'img':
      self.add_attr('src', attrs, self.assets)

  # Adds attribute value to dest (links or assets)
  def add_attr(self, attr_name, attrs, dest):
    value = self.get_attr_value(attr_name, attrs)
    if value:
      full_url = urljoin(self.base_url, value)
      dest.append(full_url)

  # Returns the value of target_attr if it exists in attrs
  def get_attr_value(self, target_attr, attrs):
    for attr, value in attrs:
      if attr == target_attr:
        return value
    return None

  # Given a URL, returns all links and assets on the page
  def crawl(self, url):
    try:
      url = url.encode('UTF-8')
      content = urlopen(url)
      encoding = content.headers.getparam('charset')
      if not encoding:
        encoding = 'UTF-8'
      content = content.read().decode(encoding)
      self.feed(content)
      return (self.href_links, self.assets)
    except HTMLParseError:
      return (self.href_links, self.assets)
    except URLError:
      return ([],[])
    except ValueError, e:
      raise

