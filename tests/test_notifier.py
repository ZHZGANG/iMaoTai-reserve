import unittest
from mock import MagicMock,Mock
from notify import PushplusNotifier,InvalidTokenError
import requests
import config
class TestPushPlusNotifier(unittest.TestCase):
    def setUp(self):
        self.requests_mock = Mock()
        requests.get = self.requests_mock.get
    def test_init_notifier_without_token(self):
        with self.assertRaises(InvalidTokenError):
            notifier = PushplusNotifier(token='', url='')

    def test_notify_successfully(self):
        self.requests_mock.get.return_value = MagicMock(status_code=200, text='success')
        notifier = PushplusNotifier(token='dummy_token', url='dummy_url')
        ok, reason = notifier.send('title', 'body')
        self.assertTrue(ok)

    def test_notify_fail(self):
        self.requests_mock.get.return_value = MagicMock(status_code=400, text='failed')
        notifier = PushplusNotifier(token='dummy_token', url='dummy_url')
        ok, reason = notifier.send('title', 'body')
        self.assertFalse(ok)
        self.assertTrue(len(reason) > 0)

    def tearDown(self):
        requests.get = requests.get

@unittest.skipIf(config.PUSH_TOKEN is None or len(config.PUSH_TOKEN)<10, 'No PushPlus token provided')
class TestRealPushPlusNotifier(unittest.TestCase):
    def test_real_sending(self):
        notifier = PushplusNotifier(token=config.PUSH_TOKEN)
        ok, reason = notifier.send('From UT', 'test_real_sending')
        self.assertTrue(ok, reason)
