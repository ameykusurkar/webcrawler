import sys, re
from collections import deque
from crawlparser import CrawlParser
from urlparse import urldefrag
from crawlerutils import add_slash, in_subdomain, StaticAssets, assets_json

if len(sys.argv) <= 1:
  print 'Please give URL to crawl as argument'
  sys.exit(0)

base_url = sys.argv[1]

# Add 'http://' if not present
if not re.match(r'https?\://*', base_url):
  base_url = 'http://' + base_url
# Remove fragments from URL
base_url = urldefrag(base_url)[0]
# Add '/' to the end of URL, so that "example.com" and "example.com/"
# are treated as the same URL string
base_url = add_slash(base_url)

# Keeping track of urls and assets
urls = deque([base_url])
all_assets = []
visited = set()

while urls:
  parser = CrawlParser(base_url)
  url = urls.popleft()
  if url in visited:
    continue
  result = parser.crawl(url)
  if not result:
    # Error occured while parsing the url
    continue
  (links, assets) = result
  visited.add(url)
  all_assets.append(StaticAssets(url, assets))
  # Add to queue only those links which are within sub-domain and not visited
  for link in links:
    link = urldefrag(link)[0]
    if in_subdomain(link, base_url) and link not in visited:
        urls.append(link)

# Print formatted JSON with static assets to STDOUT
print(assets_json(all_assets))

