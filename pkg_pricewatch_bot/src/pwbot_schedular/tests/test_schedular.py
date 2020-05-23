import unittest
from pwbot_schedular import build_bot, Schedular, settings
from pwbot_schedular.tests import utils

class TestSchedular(unittest.TestCase):

    def setUp(self):
        self.schedular = Schedular()
        self.testlist = utils.get_testlist(self.__class__.__name__)

    def test_1_addversion(self):
        """ testing add new version
        """
        for t in self.testlist:
            # unittest.TestCase.subTest(msg: Any = ...)
            with self.subTest(asins=t['asins']):
                build_bot(project=t['project'], version=t['version'])
                self.assertEqual(self.schedular.addversion(project=t['project'], version=t['version']), t['expected_number_of_spiders'])

    def test_2_schedule(self):
        """ testing add new job
        """
        for t in self.testlist:
            # unittest.TestCase.subTest(msg: Any = ...)
            with self.subTest(asins=t['asins']):
                self.assertRegex(self.schedular.schedule(project=t['project'], spider=t['spider'], _version=t['version'], asins=t['asins'], domain=t['domain']), r'^[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[0-9a-f]{12}$')

    def test_3_listjobs(self):
        """ testing get jobs
        """
        for t in self.testlist:
            # unittest.TestCase.subTest(msg: Any = ...)
            with self.subTest(asins=t['asins']):
                self.assertTrue(type(self.schedular.listjobs(project=t['project'])) is dict)

    def test_4_delversion(self):
        """ testing delete version
        """
        for t in self.testlist:
            # unittest.TestCase.subTest(msg: Any = ...)
            with self.subTest(asins=t['asins']):
                self.assertTrue(self.schedular.delversion(project=t['project'], version=t['version']))

    # def test_5_delproject(self):
    #     for t in self.testlist:
    #         # unittest.TestCase.subTest(msg: Any = ...)
    #         with self.subTest(asins=t['asins']):
    #             self.assertTrue(self.schedular.delproject(project=t['project']))

    def tearDown(self):
        self.schedular.close()
