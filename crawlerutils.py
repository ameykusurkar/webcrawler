from urlparse import urlparse
import json

# Checks that link is within the original subdomain
def in_subdomain(link, orig_url):
  link_domain = urlparse(link).netloc
  orig_domain = urlparse(orig_url).netloc
  return link_domain == orig_domain

# Adds a '/' to the end of the url if there isn't one
def add_slash(url):
  if url and url[-1] != '/':
    url += '/'
  return url

# Returns the list of StaticAssets in JSON format
def assets_json(all_assets):
  # Converts StaticAssets into dictionaries for JSON
  assets_dict = [a.__dict__ for a in all_assets]
  return json.dumps(assets_dict, indent=2)

# Encapsulates static assets
class StaticAssets:
  def __init__(self, url, assets):
    self.url = url
    self.assets = assets
