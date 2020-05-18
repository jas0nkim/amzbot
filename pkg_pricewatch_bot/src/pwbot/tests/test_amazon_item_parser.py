""" test amazon item parser
"""
import os
import unittest
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from pwbot.parsers import parse_amazon_item
from pwbot.tests import utils


def build_response(url, html_filename, domain):
    html_content = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testlists', html_filename)).read_text()
    encoding = 'utf-8'
    return HtmlResponse(url,
        request=Request(url,
            cb_kwargs={
                'crawl_variations': False,
                'domain': domain,
                'job_id': 'tempjobid',
            },
        ),
        body=html_content.encode(encoding=encoding),
    )


class TestAmazonItemParser(unittest.TestCase):
    def setUp(self):
        self.testlist = utils.get_testlist(self.__class__.__name__)
        for t in self.testlist:
            t['items'] = list(parse_amazon_item(build_response(t['url'], t['html_filename'], t['domain']),
                                                domain=t['domain'],
                                                job_id='tempjobid',
                                                crawl_variations=False),)
    
    def test_asin(self):
        for t in self.testlist:
            for i in t['items']:
                # unittest.TestCase.subTest(msg: Any = ...)
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('asin', None), t['expected_asin'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_variation_asins(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(set(i['data'].get('variation_asins', [])), set(t['expected_variation_asins']))
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_title(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('title', None), t['expected_title'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_price(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('price', None), t['expected_price'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_original_price(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('original_price', None), t['expected_original_price'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_avg_rating(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('avg_rating', None), t['expected_avg_rating'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_review_count(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('review_count', None), t['expected_review_count'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_fba(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('is_fba', None), t['expected_is_fba'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_addon(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('is_addon', None), t['expected_is_addon'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_is_pantry(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('is_pantry', None), t['expected_is_pantry'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_brand_name(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data'].get('brand_name', None), t['expected_brand_name'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))

    def test_status(self):
        for t in self.testlist:
            for i in t['items']:
                with self.subTest(asin=t['expected_asin']):
                    if i.__class__.__name__ == 'ListingItem':
                        self.assertEqual(i['data']['status'], t['expected_status'])
                    else:
                        raise Exception("Invalid 'item' object passed - {}".format(i.__class__.__name__))


if __name__ == '__main__':
    unittest.main()
