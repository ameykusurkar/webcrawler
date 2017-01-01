import unittest
from urllib2 import URLError
from crawlparser import CrawlParser
from crawlerutils import in_subdomain, assets_json, add_slash

class TestCrawler(unittest.TestCase):

  def test_invalid_url_returns_none(self):
    # base_url is not important here
    base_url = "http://example.com"
    parser = CrawlParser(base_url)
    url = "This is not a valid URL"
    result = parser.crawl(url)
    self.assertEquals(result, None)

  def test_unable_to_access_url_returns_none(self):
    base_url = "http://www.google.co.uk"
    parser = CrawlParser(base_url)
    url = "http://www.google.co.uk/notvalid"
    result = parser.crawl(url)
    self.assertEquals(result, None)

  def test_crawl_one_image_one_link(self):
    base_url = "http://www.doc.ic.ac.uk/~avk13"
    url = base_url
    parser = CrawlParser(base_url)
    expected_links = ["http://www.doc.ic.ac.uk/project/2014/163/g1416332/#introduction"]
    expected_assets = ["http://www.doc.ic.ac.uk/~avk13/2.jpg"]
    expected_result = (expected_links, expected_assets)
    result = parser.crawl(url)
    self.assertEquals(result, expected_result)

  def test_accept_subdomain(self):
    original_domain = "http://gocardless.com"
    test_link = "http://gocardless.com/developers"
    self.assertTrue(in_subdomain(test_link, original_domain))

  def test_reject_different_domain(self):
    original_domain = "http://gocardless.com"
    test_link = "http://www.google.co.uk/intl/en/about/"
    self.assertFalse(in_subdomain(test_link, original_domain))

  def test_reject_cross_domain(self):
    original_domain = "http://gocardless.com"
    test_link = "http://developer.gocardless.com/getting-started/api/introduction/"
    self.assertFalse(in_subdomain(test_link, original_domain))

  def test_add_slash_with_slash(self):
    url = "http://gocardless.com/"
    result = add_slash(url)
    self.assertEqual(url, result)

  def test_add_slash_without_slash(self):
    url = "http://gocardless.com"
    result = add_slash(url)
    self.assertEqual('http://gocardless.com/', result)

if __name__ == '__main__':
  unittest.main()
