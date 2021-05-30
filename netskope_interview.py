import unittest

from typing import List


class FindPatternInLogInput:

    def check_params(self, pattern: List[str], logline: List[str]) -> None:
        """
        Validate input arguments
        :param pattern: List of string tokens to be pattern matched
        :param logline: List of string tokens to be searched for the key in the pattern
        :return: None
        """
        if not pattern:
            raise ValueError("Parameter cannot be empty")
        if not logline:
            raise ValueError("Parameter cannot be empty")

    def find_pattern(self, pattern: List[str], logline: List[str]) -> dict:
        """
        :param pattern: List of string tokens to be pattern matched
        :param logline: List of string tokens to be searched for the key in the pattern
        :return: mapping of pattern to the string token where the pattern is found
        """
        self.check_params(logline, pattern)
        output = {}
        for key in pattern:
            for item in logline:
                if key in item:
                    if key in output.keys():
                        output.setdefault(key, []).append(item.strip())
                    else:
                        output[key] = [item.strip()]
        return output


class FindPatternInLogInputTests(unittest.TestCase):
    find_pattern_instance = FindPatternInLogInput()

    def test_find_pattern_happy_path(self):
        pattern = ["ERROR"]
        logline = ["ERROR: This is the a bad day", "INFO: This is a good day"]
        actual_value = self.find_pattern_instance.find_pattern(pattern, logline)
        expected_value = {'ERROR': ['ERROR: This is the a bad day']}
        self.assertEqual(expected_value, actual_value)

    def test_empty_args(self):
        pattern = []
        with self.assertRaises(ValueError): self.find_pattern_instance.find_pattern(pattern)
        logline = []
        with self.assertRaises(ValueError): self.find_pattern_instance.find_pattern(pattern, logline)

    def test_valid_input_complex(self):
        pattern = ["ERROR", "hello", "INFO", "WARNING", "hhh"]
        logline = ["ERROR: This is the a bad day", "INFO: This is a good day", "Warning: hello World",
                   "INFO: hello morning!", "HELLO: world!", "This is an ERROR", "WARNING WARNING: WARNING!"]
        actual_value = self.find_pattern_instance.find_pattern(pattern, logline)
        expected_value = {"ERROR": ['ERROR: This is the a bad day', "This is an ERROR"],
                          "hello": ["Warning: hello World", "INFO: hello morning!"],
                          "INFO": ["INFO: This is a good day", "INFO: hello morning!"],
                          "WARNING": ["WARNING WARNING: WARNING!"]}
        self.assertEqual(expected_value, actual_value)

    def test_no_match(self):
        pattern = ["AAA", "BBcD", "DEEJG", "WAHOOO", "Yahoo"]
        logline = ["ERROR: This is the a bad day", "INFO: This is a good day", "Warning: hello World",
                   "INFO: hello morning!", "HELLO: world!", "This is an ERROR", "WARNING WARNING: WARNING!"]
        actual_value = self.find_pattern_instance.find_pattern(pattern, logline)
        expected_value = {}
        self.assertEqual(expected_value, actual_value)

    def test_all_pattern_match(self):
        pattern = ["AAA", "BBcD", "DEEJG", "WAHOOO", "Yahoo"]
        logline = ["$$$AAAAAAA AAA", "&&&BBBB BBcD BBBB", "      ###DEEJG", "+++Yahoooo Yahoo    "]
        actual_value = self.find_pattern_instance.find_pattern(pattern, logline)
        expected_value = {"AAA": ["$$$AAAAAAA AAA"], "BBcD": ["&&&BBBB BBcD BBBB"], "DEEJG": ["###DEEJG"],
                          "Yahoo": ["+++Yahoooo Yahoo"]}
        self.assertEqual(expected_value, actual_value)
