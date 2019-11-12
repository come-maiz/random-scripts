import unittest

import testscenarios

import html_cleaner


class TestHTMLCleaner(testscenarios.WithScenarios, unittest.TestCase):

    scenarios = [
        ('noop', dict(
            html_input='hola',
            expected_output='hola')),
    ]

    def test_clean(self):
        self.assertEqual(
            html_cleaner.clean(self.html_input),
            self.expected_output)
