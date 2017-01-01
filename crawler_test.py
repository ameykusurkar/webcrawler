import subprocess, unittest

# This script tests the entire web crawler
# Script assumes that crawler.py is in the same dir

class TestWebCrawler(unittest.TestCase):

  def test_no_arguments(self):
    result = subprocess.check_output('python crawler.py', shell=True)
    expected_result = 'Please give URL to crawl as argument\n'
    self.assertEquals(result, expected_result)

  def test_simple_url(self):
    result = subprocess.check_output('python crawler.py www.doc.ic.ac.uk/~avk13', shell=True)
    expected_result = '[\n  {\n    "url": "http://www.doc.ic.ac.uk/~avk13/", \n    "assets": [\n      "http://www.doc.ic.ac.uk/~avk13/2.jpg"\n    ]\n  }\n]\n'
    self.assertEquals(result, expected_result)

if __name__ == '__main__':
  unittest.main()
