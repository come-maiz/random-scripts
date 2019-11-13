import unittest

import testscenarios

import html_cleaner


class TestHTMLCleaner(testscenarios.WithScenarios, unittest.TestCase):

    scenarios = [
        ('noop with target different than blank from links', dict(
            html_input='<a target="test">dummy</a>',
            expected_output='<a target="test">dummy</a>')),
        ('remove targe blank from links', dict(
            html_input='<a target="_blank">dummy</a>',
            expected_output='<a>dummy</a>')),
    ]

    def test_clean(self):
        self.assertEqual(
            html_cleaner.clean(self.html_input),
            self.expected_output)
