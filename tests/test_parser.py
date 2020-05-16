from unittest import TestCase, main
from common.errors import ParserException
from parser.jirawadl import ResourceParser


class ParserTestCase(TestCase):
    def test_wrong_file_input(self):
        try:
            ResourceParser('./jira-rest-no_file_at_all.wadl')
            self.assertTrue(False)
        except ParserException as error:
            self.assertEqual(error.code(), 2)

    def test_wrong_wadl_input(self):
        try:
            ResourceParser('./jira-rest-plugin_invalid.wadl')
            self.assertTrue(False)
        except ParserException as error:
            self.assertEqual(error.code(), 2)

    def test_parse_647(self):
        try:
            endpoints = ResourceParser('./jira-rest-plugin_6.4.7.wadl').get_endpoints()
            self.assertEqual(len(endpoints), 53)
            # ToDo: add more different assertions
        except ParserException as error:
            self.assertTrue(False)

    def test_parse_730(self):
        try:
            endpoints = ResourceParser('./jira-rest-plugin_7.3.0.wadl').get_endpoints()
            self.assertEqual(len(endpoints), 66)
            # ToDo: add more different assertions
        except ParserException as error:
            self.assertTrue(False)

    def test_parse_881(self):
        try:
            endpoints = ResourceParser('./jira-rest-plugin_8.8.1.wadl').get_endpoints()
            self.assertEqual(len(endpoints), 76)
            # ToDo: add more different assertions
        except ParserException as error:
            self.assertTrue(False)


if __name__ == '__main__':
    main()
