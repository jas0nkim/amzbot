import unittest, json
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from amzbot.parsers import parse_amazon_item


def build_response(url, html_filename, site):
    path = Path(html_filename)
    html_content = path.read_text()
    encoding = 'utf-8'
    return HtmlResponse(url,
        request=Request(url,
            meta={
                'parse_pictures': True,
                'parse_variations': False,
                'parse_parent_listing': True,
                'site': site,
            },
        ),
        body=html_content.encode(encoding=encoding),
    )


class TestParser(unittest.TestCase):
    def _get_testlist(self):
        # opening testlist.json file
        path = Path('htmls/testlist.json')
        content = path.read_text()
        data = json.loads(content)
        return [] if 'tests' not in data else data['tests']
    
    def setUp(self):
        self.testlist = self._get_testlist()
    
    def __test_item(self, item, t):
        self.assertEqual(1, 2)

    def test_parse_amazon_item(self):
        for t in self.testlist:
            for item in parse_amazon_item(build_response(t['url'], t['html_filename'], t['site'])):
                self.__test_item(item, t)


if __name__ == '__main__':
    unittest.main()
