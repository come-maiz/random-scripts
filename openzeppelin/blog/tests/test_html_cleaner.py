import unittest

import testscenarios

import html_cleaner


class TestHTMLCleaner(testscenarios.WithScenarios, unittest.TestCase):

    scenarios = [
        ('remove id from links', dict(
            html_input='<a id="test">dummy</a>',
            expected_output='<a>dummy</a>')),
    ]

    def test_clean(self):
        self.assertEqual(
            html_cleaner.clean(self.html_input),
            self.expected_output)
