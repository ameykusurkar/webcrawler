from crawlparser import CrawlParser
from urlparse import urlparse

# Checks that link is within the original subdomain
def in_subdomain(link, orig_url):
  link_domain = urlparse(link).netloc
  orig_domain = urlparse(orig_url).netloc
  return link_domain == orig_domain

base_url = "http://www.doc.ic.ac.uk/~ajd"
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

