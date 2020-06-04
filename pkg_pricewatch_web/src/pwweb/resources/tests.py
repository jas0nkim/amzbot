import json
from django.test import TestCase
from pwweb.resources.models import RawData, Item, ItemPrice, BuildItemPrice


class BuildItemPriceTestCase(TestCase):

    def setUp(self):
        """ insert testing data into raw_data
        """

    def test_build_amazon_com_item_price(self):
        raw_d = self._build_amazon_com_raw_data()
        bip = BuildItemPrice(raw_data=raw_d)
        item = bip.get_item()
        item_price = bip.get_item_price()

        # assert item
        self.assertEqual(item.domain, 'amazon.com')
        self.assertEqual(item.sku, 'B00004SU18')
        self.assertEqual(item.title, 'Brita Standard Replacement Filters for Pitchers and Dispensers, 3 Count, White')
        self.assertEqual(item.brand_name, 'Brita')
        self.assertEqual(item.picture_url, 'https://images-na.ssl-images-amazon.com/images/I/71FVnJO-H8L._AC_SL1500_.jpg')

        #assert item price
        self.assertEqual(item_price.domain, 'amazon.com')
        self.assertEqual(item_price.sku, 'B00004SU18')
        self.assertEqual(item_price.price, 14.97)
        self.assertEqual(item_price.original_price, 38.80)
        self.assertEqual(item_price.quantity, 1000)
        self.assertEqual(item_price.store_location, None)
        self.assertEqual(item_price.job_id, 'ffc376c5-595b-4f65-96eb-ec974eb46237')


    def test_build_amazon_ca_item_price(self):
        raw_d = self._build_amazon_ca_raw_data()
        bip = BuildItemPrice(raw_data=raw_d)
        item = bip.get_item()
        item_price = bip.get_item_price()

        # assert item
        self.assertEqual(item.domain, 'amazon.ca')
        self.assertEqual(item.sku, 'B00M0D2HQ0')
        self.assertEqual(item.title, 'The Third Wheel (Diary of a Wimpy Kid #7)')
        self.assertEqual(item.brand_name, 'by')
        self.assertEqual(item.picture_url, None)

        #assert item price
        self.assertEqual(item_price.domain, 'amazon.ca')
        self.assertEqual(item_price.sku, 'B00M0D2HQ0')
        self.assertEqual(item_price.price, 17.81)
        self.assertEqual(item_price.original_price, 17.81)
        self.assertEqual(item_price.quantity, 1000)
        self.assertEqual(item_price.store_location, None)
        self.assertEqual(item_price.job_id, '82d5c21b-46ff-4bcb-9a42-608e46c1e661')


    def _build_amazon_com_raw_data(self):
        return RawData(
            url="https://www.amazon.com/dp/B00004SU18/?th=1&psc=1",
            domain="amazon.com",
            http_status=200,
            job_id="ffc376c5-595b-4f65-96eb-ec974eb46237",
            # use json converter with JavaScript escaped option: https://www.freeformatter.com/json-formatter.html
            data=json.loads("""{\"asin\":\"B00004SU18\",\"price\":14.97,\"title\":\"Brita Standard Replacement Filters for Pitchers and Dispensers, 3 Count, White\",\"is_fba\":true,\"status\":1000,\"category\":\"Tools & Home Improvement : Kitchen & Bath Fixtures : Water Filtration & Softeners : Replacement Water Filters : Replacement Pitcher Water Filters\",\"features\":\"<div id=\\\"feature-bullets\\\" class=\\\"a-section a-spacing-medium a-spacing-top-small\\\"><ul class=\\\"a-vertical a-spacing-none\\\"><li><span class=\\\"a-list-item\\\">\\n\\t\\t\\t\\t\\t\\t\\tBPA FREE: Enjoy BPA free Brita Standard Replacement Filters made to fit all Brita pitchers and dispensers except Brita Stream pitchers. Height 5.31; Width 2.31; Length\/Depth 2.31; Weight .13 pounds\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t<\\\/span><\\\/li><li><span class=\\\"a-list-item\\\">\\n\\t\\t\\t\\t\\t\\t\\tCLEANER: Only Brita filters are certified to reduce Chlorine (taste and odor), Copper, Mercury, Zinc and Cadmium. Contaminants reduced may not be in all users\' water\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t<\\\/span><\\\/li><li><span class=\\\"a-list-item\\\">\\n\\t\\t\\t\\t\\t\\t\\tEASY INSTALLATION: A pull top cap makes filter change quick and easy with no pre-soaking necessary in order to enjoy great-tasting, filtered water in minutes\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t<\\\/span><\\\/li><li><span class=\\\"a-list-item\\\">\\n\\t\\t\\t\\t\\t\\t\\tREPLACEMENT FILTER: Replace your standard filter every 40 gallons, about every 2 months for the average household. Brita filters last 2.5x longer lasting that Zero Water\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t<\\\/span><\\\/li><li><span class=\\\"a-list-item\\\">\\n\\t\\t\\t\\t\\t\\t\\tREDUCE WASTE &amp; SAVE: One Brita standard filter can replace 300 16.9oz water bottles. Youll stay hydrated, save money and reduce plastic waste\\n\\t\\t\\t\\t\\t\\t\\t\\n\\t\\t\\t\\t\\t\\t<\\\/span><\\\/li><\\\/ul><\\\/div>\",\"is_addon\":false,\"quantity\":1000,\"is_pantry\":false,\"avg_rating\":4.7,\"brand_name\":\"Brita\",\"meta_title\":\"Amazon.com: Brita Standard Replacement Filters for Pitchers and Dispensers, 3 Count, White: Pitcher Water Filters: Kitchen & Dining\",\"description\":\"<div id=\\\"productDescription\\\" class=\\\"a-section a-spacing-small\\\">\\n        \\n\\n\\n\\n\\n\\n  \\n    \\n       \\n        \\n          \\n        <div class=\\\"disclaim\\\">\\n          \\n            \\n            \\n            \\n             Size:<strong>3 Count<\\\/strong>\\n            \\n          \\n            \\n            \\n            \\n                \u00A0|\u00A0\\n            \\n             Color:<strong>White<\\\/strong>\\n            \\n          \\n          <\\\/div>\\n        \\n      \\n    \\n  \\n\\n\\n        \\n        \\n     \\n\\t       \\n     \\n\\n     \\n\\n     \\n\\n     \\n                              \\n     \\n       \\n        <!-- show up to 2 reviews by default -->\\n        \\n          \\n          \\n            \\n              <p>Keep tap water healthier and tasting better when you regularly change your Brita replacement filter. Made to fit all Brita pitchers and dispensers, this replacement filter reduces copper, mercury and cadmium impurities that can adversely affect your health over time, while cutting chlorine taste and odor to deliver great tasting water. Designed to leave no black flecks in your water and with no pre-soak required, the Brita filters are quick and easy to use. Change your Brita filters every 40 gallons or approximately 2 months for best performance. Start drinking healthier, great tasting water with Brita today.\\n                \\n              <\\\/p>\\n            \\n            \\n          \\n        \\n        \\n        \\n      \\n      \\n    \\n    <\\\/div>\",\"merchant_id\":null,\"parent_asin\":\"B08974G1CQ\",\"picture_urls\":[\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/71FVnJO-H8L._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/81NBFs2rTTL._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/71pBRtpR7UL._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/81wmOk29qxL._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/81xB6TFchKL._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/81gnoKYcZ7L._AC_SL1500_.jpg\",\"https:\/\/images-na.ssl-images-amazon.com\/images\/I\/71sJUHJHfhL._AC_SL1500_.jpg\"],\"review_count\":12861,\"has_sizechart\":false,\"merchant_name\":\"amazon.com\",\"meta_keywords\":\"Brita Standard Replacement Filters for Pitchers and Dispensers, 3 Count, White,Brita,-\",\"original_price\":38.8,\"specifications\":[{\"Product Dimensions\":\"14.81 x 9.94 x 6.13 inches\"},{\"Item Weight\":\"12.8 ounces\"},{\"Department\":\"Office\"},{\"Manufacturer\":\"Brita\"},{\"ASIN\":\"B00004SU18\"},{\"Item model number\":\"-\"},{\"Customer Reviews\":\"\"},{\"Best Sellers Rank\":\"\"},{\"Is Discontinued By Manufacturer\":\"No\"},{\"Date First Available\":\"October 2, 2001\"}],\"variation_asins\":[\"B00004SU18\",\"B00006J6WX\"],\"meta_description\":\"Shop Brita at the Amazon Water Coolers & Filters store. Free Shipping on eligible items. Everyday low prices, save up to 50%.\",\"variation_specifics\":{\"Size\":\"3 Count\",\"Color\":\"White\"}}"""),
        )

    def _build_amazon_ca_raw_data(self):
        return RawData(
            url="https://www.amazon.ca/Third-Wheel-Diary-Wimpy-Kid/dp/B00M0D2HQ0/ref=tmm_hrd_swatch_0?_encoding=UTF8&qid=&sr=",
            domain="amazon.ca",
            http_status=200,
            job_id="82d5c21b-46ff-4bcb-9a42-608e46c1e661",
            # use json converter with JavaScript escaped option: https://www.freeformatter.com/json-formatter.html
            data=json.loads("""{\"asin\":\"B00M0D2HQ0\",\"price\":17.81,\"title\":\"The Third Wheel (Diary of a Wimpy Kid #7)\",\"is_fba\":false,\"status\":1000,\"category\":\"Books : Children\'s Books : Literature & Fiction\",\"features\":null,\"is_addon\":false,\"quantity\":1000,\"is_pantry\":false,\"avg_rating\":4.7,\"brand_name\":\"by\",\"meta_title\":\"The Third Wheel (Diary of a Wimpy Kid #7): Kinney, Jeff: 9781419741937: Books - Amazon.ca\",\"description\":null,\"merchant_id\":null,\"parent_asin\":null,\"picture_urls\":[],\"review_count\":5300,\"has_sizechart\":false,\"merchant_name\":\"amazon.ca\",\"meta_keywords\":\"Kinney, Jeff,The Third Wheel (Diary of a Wimpy Kid #7),Amulet Books,B00M0D2HQ0,Best friends,Dance parties,Diaries,Humorous stories,Middle school students,Middle schools,Middle schools;Fiction.,Schools,Schools;Fiction.,Valentine\'s Day,Valentine\'s Day;Fiction.,JUVENILE FICTION \/ Humorous Stories,JUVENILE FICTION,Humorous Stories,JUVENILE FICTION \/ Comics & Graphic Novels \/ General,Comics & Graphic Novels,General,teenage romance;dances;finding a date;finding love;growing up;love poem;coming of age;friendship;middle school,JUVENILE FICTION \/ Comics & Graphic Novels \/ General,JUVENILE FICTION \/ Humorous Stories,Juvenile Fiction\/Comics & Graphic Novels - General\",\"original_price\":17.81,\"specifications\":null,\"variation_asins\":[],\"meta_description\":\"The Third Wheel (Diary of a Wimpy Kid #7): Kinney, Jeff: 9781419741937: Books - Amazon.ca\",\"variation_specifics\":null}"""),
        )

    def _build_walmart_com_raw_data(self):
        pass

    def _build_walmart_ca_raw_data(self):
        pass

    def _build_canadiantire_ca_raw_data(self):
        pass
