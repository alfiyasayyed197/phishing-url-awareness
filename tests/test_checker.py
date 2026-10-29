"""Automated checks for the reserved workbook examples and safe improvements."""

import unittest

from phishing_checker import has_warnings, inspect_url


class InspectUrlTests(unittest.TestCase):
    def test_five_workbook_samples(self):
        cases = [
            ("https://www.example.com/login", "No listed warning signs"),
            ("http://192.0.2.10/account", "IP address"),
            ("http://example.com@sample.invalid/login", "@ symbol"),
            ("https://a.b.c.d.e.example.invalid/path", "hostname segments"),
            ("https://xn--example.invalid/", "punycode-style"),
        ]
        for url, expected_text in cases:
            with self.subTest(url=url):
                self.assertTrue(any(expected_text in finding for finding in inspect_url(url)))

    def test_empty_input_is_friendly(self):
        self.assertEqual(inspect_url("  "), ["No URL entered."])

    def test_malformed_ipv6_does_not_crash(self):
        self.assertEqual(inspect_url("http://[bad"), ["This text is not a valid URL format."])

    def test_long_url_is_flagged(self):
        self.assertTrue(any("over 100 characters" in finding for finding in inspect_url("https://example.invalid/" + "a" * 101)))

    def test_summary_only_for_warnings(self):
        self.assertTrue(has_warnings(inspect_url("http://192.0.2.10/account")))
        self.assertFalse(has_warnings(inspect_url("")))
        self.assertFalse(has_warnings(inspect_url("https://www.example.com/login")))


if __name__ == "__main__":
    unittest.main()
