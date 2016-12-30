import unittest

class TestStuff(unittest.TestCase):
  def test_add(self):
    self.assertEqual(3+4, 7)

if __name__ == '__main__':
  unittest.main()
