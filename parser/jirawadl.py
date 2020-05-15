from xml.etree.ElementTree import Element, ParseError, parse
from common.errors import ParserException


class ResourceParser:
    __document = None

    def __init__(self, wadl_file: str):
        try:
            self.__document = parse(wadl_file)
            self.__is_jira_wadl()
        except ParseError as error:
            raise ParserException('WADL resource parser error: {}'.format(error.msg))

    def get_endpoints(self) -> dict:
        endpoints = {}
        resources = self.__get_resources()
        for child in resources:
            if child.attrib.get('path') is None:
                raise ParserException('Could not parse resources')
            endpoints[child.attrib['path']] = self.__get_methods(child)
        return endpoints

    def __is_jira_wadl(self):
        for child in self.__document.getroot():
            if child.attrib.get('title') and 'Jira' in child.attrib['title']:
                return
        raise ParserException('Provided WADL document is invalid')

    def __get_resources(self) -> Element:
        root = self.__document.getroot()
        for child in root:
            prefix, namespace, tag = child.tag.partition('}')
            if 'resources' == tag:
                return child
        raise ParserException('Could not find resources')

    def __get_methods(self, resource: Element) -> dict:
        return {}
