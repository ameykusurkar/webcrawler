import unittest
from crawlparser import CrawlParser

class TestCrawler(unittest.TestCase):

  def test_invalid_url_raises_exception(self):
    # base_url is not important here
    base_url = "http://example.com"
    parser = CrawlParser(base_url)
    with self.assertRaises(ValueError):
      url = "This is not a valid URL"
      parser.crawl(url)

  def test_crawl_one_image_one_link(self):
    base_url = "http://www.doc.ic.ac.uk/~avk13"
    url = base_url
    parser = CrawlParser(base_url)
    expected_links = ["http://www.doc.ic.ac.uk/project/2014/163/g1416332/#introduction"]
    expected_assets = ["http://www.doc.ic.ac.uk/~avk13/2.jpg"]
    expected_result = (expected_links, expected_assets)
    result = parser.crawl(url)
    self.assertEquals(result, expected_result)


if __name__ == '__main__':
  unittest.main()
