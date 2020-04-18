import unittest, json
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from amzbot.parsers import parse_amazon_item


def build_response(url, html_filename, site):
    html_content = Path(html_filename).read_text()
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
        content = Path('htmls/testlist.json').read_text()
        data = json.loads(content)
        return [] if 'tests' not in data else data['tests']
    
    def setUp(self):
        self.testlist = self._get_testlist()
    
    def __test_item(self, item, t):
        if item.instance.__class__.__name__ == 'AmazonParentListing':
            self.__test_parent_listing_item(item, t)
        elif item.instance.__class__.__name__ == 'AmazonListing':
            self.__test_listing_item(item, t)
        else:
            raise Exception("Invalid 'item' passed")

    def __test_parent_listing_item(self, item, t):
        self.assertEqual(item['review_count'], t['expected_review_count'])
        self.assertEqual(item['avg_rating'], t['expected_avg_rating'])

    def __test_listing_item(self, item, t):
        self.assertEqual(item['asin'], t['expected_asin'])
        self.assertEqual(item['title'], t['expected_title'])
        self.assertEqual(item['price'], t['expected_price'])
        self.assertEqual(item['is_fba'], t['expected_is_fba'])
        self.assertEqual(item['is_addon'], t['expected_is_addon'])
        self.assertEqual(item['is_pantry'], t['expected_is_pantry'])
        self.assertEqual(item['brand_name'], t['expected_brand_name'])
        self.assertEqual(item['status'], t['expected_status'])

    def test_parse_amazon_item(self):
        for t in self.testlist:
            for item in parse_amazon_item(build_response(t['url'], t['html_filename'], t['site'])):
                self.__test_item(item, t)


if __name__ == '__main__':
    unittest.main()
