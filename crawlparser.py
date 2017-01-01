from urllib2 import urlopen, URLError
from HTMLParser import HTMLParser, HTMLParseError
from urlparse import urljoin
from crawlerutils import add_slash

"""
Given a URL, parser finds all the links and static
assets (images, javascript, stylesheets) on the page.
Only the method CrawlParser.crawl(url) is called externally,
other methods are used interally during parsing.
"""
class CrawlParser(HTMLParser):

  def __init__(self, base_url):
    # base_url needs to end with '/' for urljoin
    # used for converting relative paths into full urls
    self.base_url = add_slash(base_url)
    self.href_links = []
    self.assets = []
    HTMLParser.__init__(self)

  # Extracts links and assets as it encounters relevant tags
  def handle_starttag(self, tag, attrs):
    if tag == 'a':
      # Store href links
      self.add_attr('href', attrs, self.href_links)
    # Only add to assets if link is a stylesheet
    if tag == 'link' and self.get_attr_value('rel', attrs) == 'stylesheet':
      # Store stylesheets as static assets
      self.add_attr('href', attrs, self.assets)
    if tag == 'script' or tag == 'img':
      # Store images and javascript as static assets
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
  # Returns None if unable access URL
  def crawl(self, url):
    try:
      url = url.encode('UTF-8')
      content = urlopen(url)
      encoding = content.headers.getparam('charset')
      if not encoding:
        encoding = 'UTF-8'
      # Characters that cannot be recognised are ignored
      content = content.read().decode(encoding, "ignore")
      self.feed(content)
      return (self.href_links, self.assets)
    except HTMLParseError:
      # Return whatever links and assets found so far
      return (self.href_links, self.assets)
    except (URLError, ValueError):
      # Could not access URL
      return None

