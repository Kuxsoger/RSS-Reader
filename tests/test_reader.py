import contextlib
import httpretty
import io
import logging
import os
import sys
import unittest

from rss_reader import __version__
from rss_reader import cache
from rss_reader import reader


class TestReader(unittest.TestCase):
    """Test rss reader with all possible arguments."""

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        cache.CACHE_FILE = '.testcache'

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'example.xml')
        with open(path, 'rb') as f:
            xml = f.read()

        httpretty.register_uri(
            httpretty.GET,
            status=200,
            body=xml,
            uri='https://example.com/rss/'
        )

    @classmethod
    def tearDownClass(cls):
        httpretty.reset()
        httpretty.disable()

    def tearDown(self):
        path = os.path.join(os.path.dirname(cache.__file__), '.testcache')
        if os.path.isfile(path):
            os.remove(path)

    def test_reading(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.run(['https://example.com/rss/'])

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_reading.txt')
        with open(path) as f:
            expected_output = f.read()

        self.assertEqual(out.getvalue(), expected_output)

    def test_json(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.run(['--json', 'https://example.com/rss/'])

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_json.txt')
        with open(path) as f:
            expected_output = f.read()

        self.assertEqual(out.getvalue(), expected_output)

    def test_limit(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.run(['--limit', '2', 'https://example.com/rss/'])

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_limit.txt')
        with open(path) as f:
            expected_output = f.read()

        self.assertEqual(out.getvalue(), expected_output)

    def test_verbose(self):
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_verbose.txt')
        with open(path) as f:
            expected_output = f.read()

        with self.assertLogs(logging.getLogger(), level='INFO') as cm:
            reader.run(['--verbose', 'https://example.com/rss/'])

            # sqlitedict logs openning table like "opening table in {full_path}" so we remove {full_path}
            cm.output[8] = ' '.join(cm.output[8].split(' ')[:-1])

            self.assertEqual('\n'.join(cm.output), expected_output)

    def test_version(self):
        out = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(out):
                reader.run(['--version'])

        self.assertEqual(out.getvalue(), 'RSS Reader {}\n'.format(__version__))

    def test_help(self):
        out = io.StringIO()
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(out):
                sys.argv[0] = 'rss-reader'
                reader.run(['-h'])

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_help.txt')
        with open(path) as f:
            expected_output = f.read()

        self.assertEqual(out.getvalue(), expected_output)

    def test_caching(self):
        reader.run(['https://example.com/rss/'])

        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            reader.run(['--date', '20191211', 'https://example.com/rss/'])

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'expected_caching.txt')
        with open(path) as f:
            expected_output = f.read()

        self.assertEqual(out.getvalue(), expected_output)
