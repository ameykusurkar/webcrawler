from crawlparser import CrawlParser

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

