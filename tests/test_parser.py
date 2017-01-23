import unittest
from search import Search


class TestParser(unittest.TestCase):

    def setUp(self):
        urls = ['example.com']
        self.searcher = Search(urls)

    def tearDown(self):
        self.searcher = None

    def test_text_single_result(self):
        content = '<p>@foobar</p>'
        self.searcher.parse_text(content, 'example.com')
        output = self.searcher.get_results
        self.assertEqual('@foobar', output[0]['results'][0])

    def test_links_single_result(self):
        content = '<a href="https://twitter.com">@foo</a>'
        self.searcher.parse_links(content, 'example.com')
        output = self.searcher.get_results
        self.assertEqual('@foo', output[0]['results'][0])

    def test_invalid_link(self):
        content = '<a href="https://google.com">@foo</a>'
        self.searcher.parse_links(content, 'example.com')
        output = self.searcher.get_results
        self.assertEqual(0, len(output[0]['results']))

if __name__ == '__main__':
    unittest.main()
