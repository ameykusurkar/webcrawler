from collections import deque
from crawlparser import CrawlParser
from urlparse import urldefrag
from crawlerutils import add_slash, in_subdomain, StaticAssets, assets_json

base_url = "http://www.doc.ic.ac.uk/~avk13"
base_url = urldefrag(base_url)[0]
base_url = add_slash(base_url)
urls = deque([base_url])
all_assets = []
visited = set()
count = 0
while urls:
  parser = CrawlParser(base_url)
  url = urls.popleft()
  if url in visited:
    continue
  if count % 1 == 0:
    print("{} Visiting: {}".format(count, url))
    print("{} link(s) left in queue".format(len(urls)))
  try:
    result = parser.crawl(url)
    if not result:
      continue
    (links, assets) = result
    count += 1
    visited.add(url)
    all_assets.append(StaticAssets(url, assets))
    for link in links:
      link = urldefrag(link)[0]
      if in_subdomain(link, base_url) and link not in visited:
        urls.append(link)
  except ValueError:
    visited.add(url)
    print("Invalid URL.")
    print(url)

print("Visited {} site(s)".format(count))
f = open('visited.txt', 'w')
f.write(assets_json(all_assets))

"""
for l in links:
  print(l)
print("{} link(s) found.".format(len(links)))
for a in assets:
  print(a)
print("{} assets(s) found.".format(len(assets)))
"""
