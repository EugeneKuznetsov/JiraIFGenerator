from copy import deepcopy
from unittest import TestCase, main
from parser.jirawadl import ResourceParser
from parser.resourcebundle import Bundle


class ResourceBundleTestCase(TestCase):
    resources = ResourceParser('../wadl/jira-rest-plugin_8.8.1.wadl').get_resources()
    packed_resources = Bundle().pack(resources)

    def test_packed_resources(self):
        self.assertEqual(len(self.packed_resources), 57)

    def test_endpoint_issue(self):
        endpoint = deepcopy(self.packed_resources['issue'])
        method_names = [method['id'] for method in endpoint]
        self.assertIn('createIssue', method_names)

    def test_endpoint_priorityschemes(self):
        endpoint = deepcopy(self.packed_resources['priorityschemes'])
        method_names = [method['id'] for method in endpoint]
        self.assertIn('deletePriorityScheme', method_names)


if __name__ == '__main__':
    main()
