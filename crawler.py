from collections import deque
from urlparse import urlparse, urldefrag
from crawlparser import CrawlParser

# Checks that link is within the original subdomain
def in_subdomain(link, orig_url):
  link_domain = urlparse(link).netloc
  orig_domain = urlparse(orig_url).netloc
  return link_domain == orig_domain

def add_slash(url):
  if url and url[-1] != '/':
    url += '/'
  return url

base_url = "http://www.doc.ic.ac.uk/~fpj14"
base_url = urldefrag(base_url)[0]
base_url = add_slash(base_url)
urls = deque([base_url])
visited = set()
count = 1
while urls:
  parser = CrawlParser(base_url)
  url = urls.popleft()
  if url in visited or url.endswith('.pdf'):
    continue
  if count % 1 == 0:
    print("{} Visiting: {}".format(count, url))
    print("{} link(s) left in queue".format(len(urls)))
  try:
    (links, assets) = parser.crawl(url)
    count += 1
    visited.add(url)
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
for link in visited:
  f.write(link)
  f.write('\n')

"""
for l in links:
  print(l)
print("{} link(s) found.".format(len(links)))
for a in assets:
  print(a)
print("{} assets(s) found.".format(len(assets)))
"""
