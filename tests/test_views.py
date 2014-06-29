import env
from unittest import TestCase, main
from os import path
import url_short.views
from url_short import app
import json
import redis

TESTDIR = path.dirname(path.realpath(__file__))

class UrlShortTestCase(TestCase):
    def setUp(self):
        redis.from_url(app.config['REDISTOGO_URL']).flushall() # clean up old test results
        self.app = app.test_client()

    def test_shorten_new_url(self):
        long_url = 'test'
        response = self.app.get('/shorten?url=%s' % long_url)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['long_url'], long_url)
        self.assertEqual(int(data['visits']), 0)
        self.assertEqual(len(data['short_url']), 3)

    def test_shorten_existing_url(self):
        long_url = 'test'
        response = self.app.get('/shorten?url=%s' % long_url)
        data = json.loads(response.data)
        short_url = data['short_url']

        # try shortening the same url again. You should get back the
        # same short url as before
        response = self.app.get('/shorten?url=%s' % long_url)
        self.assertEqual(data['short_url'], short_url)
        self.assertTrue(data['success'])
        self.assertEqual(data['long_url'], long_url)
        self.assertEqual(int(data['visits']), 0)

    def test_lengthen_existing_short_url(self):
        long_url = 'test'
        response = self.app.get('/shorten?url=%s' % long_url)
        data = json.loads(response.data)
        short_url = data['short_url']

        # try lengthening the same url again. You should get back the
        # original long url
        response = self.app.get('/%s' % short_url)
        data = json.loads(response.data)
        self.assertEqual(data['short_url'], short_url)
        self.assertTrue(data['success'])
        self.assertEqual(data['long_url'], long_url)
        self.assertEqual(int(data['visits']), 1)

if __name__ == '__main__':
    main()
