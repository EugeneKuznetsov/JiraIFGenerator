import logging
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
        except FileNotFoundError as error:
            raise ParserException('WADL file not found error')

    def get_endpoints(self) -> list:
        return self.__traverse_resources(self.__get_resource_container())[0]['sub_resources']

    def __is_jira_wadl(self):
        for child in self.__document.getroot():
            if child.attrib.get('title') and 'jira' in child.attrib['title'].lower():
                return
        raise ParserException('Provided WADL document is invalid')

    def __get_resource_container(self) -> Element:
        root = self.__document.getroot()
        for child in root:
            if 'resources' == self.__get_tag(child):
                return child
        raise ParserException('Could not find resources')

    def __traverse_resources(self, parent: Element, parent_path: str = None) -> list:
        parent_tag = self.__get_tag(parent)
        if 'resource' == parent_tag and parent_path is None:
            parent_path = parent.attrib['path']
        elif parent_path is not None:
            if parent_path[-1] == '/' and parent.attrib['path'][0] == '/':
                parent_path = parent_path[0:-1]
            elif parent_path[-1] != '/' and parent.attrib['path'][0] != '/':
                parent_path += '/'
            parent_path += parent.attrib['path']
        resources = [{'uri': parent_path}]
        for child in parent:
            tag = self.__get_tag(child)
            if 'resource' == tag:
                for sub_resource in self.__traverse_resources(child, parent_path):
                    if resources[-1].get('sub_resources') is None:
                        resources[-1]['sub_resources'] = []
                    resources[-1]['sub_resources'].append(sub_resource)
            elif 'method' == tag:
                if resources[-1].get('methods') is None:
                    resources[-1]['methods'] = []
                resources[-1]['methods'].append(self.__parse_method(child))
            elif 'doc' == tag:
                if resources[-1].get('doc') and child.text:
                    logging.warning('Unexpected amount (more than 1) of doc when parsing resources')
                if child.text:
                    resources[-1]['doc'] = child.text
            elif 'param' == tag:
                if resources[-1].get('parameters') is None:
                    resources[-1]['parameters'] = []
                resources[-1]['parameters'].append(self.__parse_param(child))
            else:
                logging.warning('Unexpected tag {} when parsing resource'.format(tag))
        return resources

    def __parse_method(self, parent: Element) -> dict:
        method_id = parent.attrib['id']
        http_request_name = parent.attrib['name']
        method = {'id': method_id, 'name': http_request_name}
        responses = []
        for child in parent:
            tag = self.__get_tag(child)
            if 'request' == tag:
                method['request'] = self.__parse_request(child)
            elif 'response' == tag:
                responses.append(self.__parse_response(child))
            elif 'doc' == tag:
                if method.get('doc') and child.text:
                    logging.warning('Unexpected amount (more than 1) of doc when parsing method')
                if child.text:
                    method['doc'] = child.text
            else:
                logging.warning('Unexpected tag {} when parsing method'.format(tag))
        if len(responses):
            method['responses'] = responses
        return method

    def __parse_request(self, parent: Element) -> dict:
        request = {}
        for child in parent:
            tag = self.__get_tag(child)
            if 'param' == tag:
                if request.get('parameters') is None:
                    request['parameters'] = []
                request['parameters'].append(self.__parse_param(child))
            elif 'representation' == tag:
                if request.get('representation') is not None:
                    logging.warning('Unexpected amount (more than 1) of representation when parsing request')
                request['representation'] = self.__parse_representation(child)
            else:
                logging.warning('Unexpected tag {} when parsing request'.format(tag))
        return request

    def __parse_response(self, parent: Element) -> dict:
        response = parent.attrib
        for child in parent:
            tag = self.__get_tag(child)
            if 'representation' == tag:
                if response.get('representations') is None:
                    response['representations'] = []
                response['representations'].append(self.__parse_representation(child))
            elif 'doc' == tag:
                if response.get('doc') and child.text:
                    logging.warning('Unexpected amount (more than 1) of doc when parsing response')
                if child.text:
                    response['doc'] = child.text
            else:
                logging.warning('Unexpected tag {} when parsing response'.format(tag))
        return response

    def __parse_param(self, parent: Element) -> dict:
        parameter = {
            'name': parent.attrib['name'],
            'style': parent.attrib['style'],
            'type': self.__parse_param_type(parent.attrib['type'])
        }
        if parent.attrib.get('default'):
            parameter['default'] = parent.attrib['default']
        for child in parent:
            tag = self.__get_tag(child)
            if 'doc' == tag:
                if parameter.get('doc') and child.text:
                    logging.warning('Unexpected amount (more than 1) of doc when parsing param')
                if child.text:
                    parameter['doc'] = child.text
            else:
                logging.warning('Unexpected tag {} when parsing param'.format(tag))
        return parameter

    def __parse_representation(self, parent: Element) -> dict:
        representation = {}
        if parent.attrib.get('mediaType'):
            representation['mediaType'] = parent.attrib['mediaType']
        if parent.attrib.get('element'):
            representation['element'] = parent.attrib['element']
        for child in parent:
            tag = self.__get_tag(child)
            if 'param' == tag:
                if representation.get('parameters') is None:
                    representation['parameters'] = []
                representation['parameters'].append(self.__parse_param(child))
            elif 'doc' == tag:
                if representation.get('doc') and child.text:
                    logging.warning('Unexpected amount (more than 1) of doc when parsing representation')
                if child.text:
                    representation['doc'] = child.text
            else:
                logging.warning('Unexpected tag {} when parsing representation'.format(tag))
        return representation

    @staticmethod
    def __parse_param_type(param_type: str) -> str:
        return param_type.replace('xs:', '')

    @staticmethod
    def __get_tag(element: Element) -> str:
        prefix, namespace, tag = element.tag.partition('}')
        return tag
