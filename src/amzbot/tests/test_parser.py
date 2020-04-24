import os, unittest, json
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from amzbot.parsers import parse_amazon_item
from amzbot.tests import utils


def build_response(url, html_filename, domain):
    html_content = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmls', html_filename)).read_text()
    encoding = 'utf-8'
    return HtmlResponse(url,
        request=Request(url,
            meta={
                'parse_pictures': True,
                'parse_variations': False,
                'parse_parent_listing': True,
                'domain': domain,
            },
        ),
        body=html_content.encode(encoding=encoding),
    )


class TestParser(unittest.TestCase):
    def setUp(self):
        self.testlist = utils.get_testlist(self.__class__.__name__)
        for t in self.testlist:
            t['items'] = list(parse_amazon_item(build_response(t['url'], t['html_filename'], t['domain'])))
    
    def test_asin(self):
        for t in self.testlist:
            for i in t['items']:
                # unittest.TestCase.subTest(msg: Any = ...)
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['asin'], t['expected_asin'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_variation_asins(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        pass
                    elif i.__class__.__name__ == 'ParentListingItem':
                        self.assertEqual(set(i['asins']), set(t['expected_variation_asins']))
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_title(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['title'], t['expected_title'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_price(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['price'], t['expected_price'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_original_price(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['original_price'], t['expected_original_price'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_avg_rating(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        pass
                    elif i.__class__.__name__ == 'ParentListingItem':
                        self.assertEqual(i['avg_rating'], t['expected_avg_rating'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_review_count(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        pass
                    elif i.__class__.__name__ == 'ParentListingItem':
                        self.assertEqual(i['review_count'], t['expected_review_count'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_fba(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['is_fba'], t['expected_is_fba'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_addon(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['is_addon'], t['expected_is_addon'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_pantry(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['is_pantry'], t['expected_is_pantry'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_brand_name(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['brand_name'], t['expected_brand_name'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_status(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['status'], t['expected_status'])
                    elif i.__class__.__name__ == 'ParentListingItem':
                        pass
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))


if __name__ == '__main__':
    unittest.main()
