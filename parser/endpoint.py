import re
from common.errors import UnsupportedParameterTypeException, UnsupportedParameterStyleException
import json



class Endpoint:
    header_filename = ''
    source_filename = ''
    header_content = ''
    source_content = ''
    class_name = ''
    __methods = []
    __generator_version = {'major': 0, 'minor': 0}

    def __init__(self, name: str, methods: list, version: dict):
        self.__generator_version = version
        self.__methods = methods
        name = self.__cleanup_file_name(name)
        self.header_filename = name + '.h'
        self.source_filename = name + '.cpp'
        self.class_name = self.__cleanup_class_name(name)
        self.__parse_header()
        self.__parse_source()

    def __parse_header(self):
        header = self.__generate_disclaimer()
        header += '#pragma once\n\n#include "endpoint.h"\n\nnamespace GeneratedEndpoints {\n\n'
        header += 'class {} : public Endpoint\n'.format(self.class_name)
        header += '{\n    Q_OBJECT\n\nprotected:\n    ' + self.class_name
        header += '(const QJSValue &callback);\n\npublic slots:\n'
        slots = []
        slot_buddies = []
        for method in self.__methods:
            slot, buddies = self.__parse_header_method(method)
            slots.append('    ' + slot)
            for buddy in buddies:
                slot_buddies.append('    ' + buddy)
        header += '\n'.join(slots)
        header += '\n\nprotected:\n'
        header += '\n'.join(slot_buddies)
        header += '\n};\n\n}\n'
        self.header_content = header

    def __parse_header_method(self, method: dict) -> tuple:
        slot = self.__parse_header_slot(method)
        request = self.__parse_header_pre_request(method)
        success = self.__parse_header_method_success(method)
        error = self.__parse_header_method_error(method)
        return slot, [request, success, error]

    def __parse_header_slot(self, method: dict) -> str:
        slot = 'virtual void {}('.format(self.__cleanup_method_name(method['id']))
        parameters = []
        if method.get('parameters'):
            base_uri = method['path']
            base_uri_parameters = re.findall('{([a-zA-Z]+)}', base_uri)
            for base_uri_parameter in base_uri_parameters:
                for parameter in method['parameters']:
                    if parameter['name'] == base_uri_parameter:
                        parameters.append('{}{}'.format(self.__translate_type(parameter['type']), parameter['name']))
                        break
        if method.get('request') and method['request'].get('parameters'):
            for parameter in method['request']['parameters']:
                parameters.append('{}{}'.format(self.__translate_type(parameter['type']),
                                                self.__cleanup_parameter_name(parameter['name'])))
        slot += ', '.join(parameters)
        slot += ');'
        return slot

    def __parse_source(self):
        source = self.__generate_disclaimer()
        source += '#include <QUrlQuery>\n#include "network/reply.h"\n#include "{}"\n\n'.format(self.header_filename)
        source += 'GeneratedEndpoints::{}::{}(const QJSValue &callback)\n'.format(self.class_name, self.class_name)
        source += '    : Endpoint(callback)\n{\n}\n\n'
        slots = []
        slot_buddies = []
        for method in self.__methods:
            slot, buddies = self.__parse_source_method(method)
            slots.append(slot)
            for buddy in buddies:
                slot_buddies.append(buddy)
        source += '\n\n'.join(slots)
        source += '\n\n'
        source += '\n\n'.join(slot_buddies)
        self.source_content = source

    def __parse_source_method(self, method: dict) -> tuple:
        slot = self.__parse_source_slot(method)
        request = self.__parse_source_pre_request(method)
        success = self.__parse_source_method_success(method)
        error = self.__parse_source_method_error(method)
        return slot, [request, success, error]

    def __parse_source_slot(self, method: dict) -> str:
        slot = 'void GeneratedEndpoints::{}::{}('.format(self.class_name, self.__cleanup_method_name(method['id']))
        parameters = []
        if method.get('parameters'):
            base_uri = method['path']
            base_uri_parameters = re.findall('{([a-zA-Z]+)}', base_uri)
            for base_uri_parameter in base_uri_parameters:
                for parameter in method['parameters']:
                    if parameter['name'] == base_uri_parameter:
                        parameters.append('{}{}'.format(self.__translate_type(parameter['type']), parameter['name']))
                        break
        if method.get('request') and method['request'].get('parameters'):
            for parameter in method['request']['parameters']:
                parameters.append('{}{}'.format(self.__translate_type(parameter['type']),
                                                self.__cleanup_parameter_name(parameter['name'])))
        slot += ', '.join(parameters)
        slot += ')\n{\n'
        slot += self.__parse_source_slot_impl(method)
        slot += '\n}'
        return slot

    def __parse_source_slot_impl(self, method: dict) -> str:
        impl = ''
        base_uri = '"{}"'.format(method['path'])
        if method.get('parameters'):
            args = []
            base_uri_parameters = re.findall('{([a-zA-Z]+)}', base_uri)
            for position, base_uri_parameter in enumerate(base_uri_parameters, start=1):
                for parameter in method['parameters']:
                    if parameter['name'] == base_uri_parameter:
                        base_uri = base_uri.replace('{' + base_uri_parameter + '}', '%{}'.format(position))
                        args.append('arg({})'.format(parameter['name']))
                        break
            base_uri = 'QString({}).{}'.format(base_uri, '.'.join(args))
        impl += '    setBaseUri(QUrl({}));\n'.format(base_uri)
        impl += self.__parse_source_slot_impl_parameters(method)
        impl += self.__parse_source_slot_impl_connection(method)
        return impl

    def __parse_source_slot_impl_parameters(self, method: dict) -> str:
        impl = ''
        if method.get('request') and method['request'].get('parameters'):
            query_parameters = []
            header_parameters = []
            remove_empty = []
            for parameter in method['request']['parameters']:
                if parameter['style'] == 'query':
                    argument = parameter['name']
                    if parameter['type'] != 'string':
                        argument = 'QVariant({}).toString()'.format(argument)
                    query_parameters.append('{' + '"{}", {}'.format(parameter['name'], argument) + '}')
                    if parameter['type'] == 'string':
                        remove_empty.append('    if ({}.isEmpty())\n        query.removeQueryItem({});\n'
                                            .format(parameter['name'], parameter['name']))
                elif parameter['style'] == 'header':
                    converted_parameter = self.__cleanup_parameter_name(parameter['name'])
                    if parameter['type'] != 'string':
                        converted_parameter = 'QVariant({}).toString()'.format(converted_parameter)
                    header_parameters.append({parameter['name']: converted_parameter})
                else:
                    raise UnsupportedParameterStyleException(parameter['style'])
            if len(query_parameters):
                query_parameters = '    QUrlQuery query({\n        ' + ',\n        ' \
                    .join(query_parameters) + '\n    });\n'
                impl += query_parameters
                impl += ''.join(remove_empty)
                impl += '    setBaseUriQuery(query);\n'
            if len(header_parameters):
                for header in header_parameters:
                    for header_key, header_value in header.items():
                        impl += '    setHeader("{}", {});\n'.format(header_key, header_value)
        return impl

    def __parse_source_slot_impl_connection(self, method: dict) -> str:
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        pre_request_method_name = 'on{}Request()'.format(method_name)
        impl = '    connect({}, &Reply::ready, [this](const int statusCode, const QByteArray &data)'\
            .format(pre_request_method_name) + ' {\n'
        status_map = []
        impl += '        const StatusMap codes = {\n'
        if method.get('responses'):
            for response in method['responses']:
                status = response['status']
                success = 'true' if status.startswith('2') or status.startswith('3') else 'false'
                status_map.append('{' + status + ', ' + success + '}')

            indent = '            '
            impl += indent
            impl += (',\n' + indent).join(status_map)
            impl += '\n'
        impl += '        };\n'
        impl += '        auto successStatus = codes.find(statusCode);\n'
        impl += '        if (successStatus != codes.cend() && successStatus.value())\n'
        impl += '            callback(statusCode, data, codes, on{}Success(data));\n'.format(method_name)
        impl += '        else\n'
        impl += '            callback(statusCode, data, codes, on{}Error(data));\n'.format(method_name)
        impl += '    });'
        return impl

    def __parse_source_pre_request(self, method: dict) -> str:
        http_method = method['name']
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        request = 'Reply *GeneratedEndpoints::{}::on{}Request(/* {} */)\n'\
            .format(self.class_name, method_name, http_method)
        request += '{\n'
        if http_method == 'POST' or http_method == 'PUT':
            request += '    return nullptr;\n'
        elif http_method == 'GET':
            request += '    return get();\n'
        elif http_method == 'DELETE':
            request += '    return deleteResource();\n'
        request += '}'
        return request

    def __parse_source_method_success(self, method: dict) -> str:
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        impl = 'QJSValueList GeneratedEndpoints::{}::on{}Success(const QByteArray &data)\n'\
            .format(self.class_name, method_name)
        impl += '{\n'
        impl += '    return {};'
        impl += '\n}'
        return impl

    def __parse_source_method_error(self, method: dict) -> str:
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        impl = 'QJSValueList GeneratedEndpoints::{}::on{}Error(const QByteArray &data)\n' \
            .format(self.class_name, method_name)
        impl += '{\n'
        impl += '    return {};'
        impl += '\n}'
        return impl

    def __generate_disclaimer(self) -> str:
        return '/***\n* Jira Interface Generator v{}.{}\n*\n* Automatically generated Endpoint\n*/\n\n'\
            .format(self.__generator_version['major'], self.__generator_version['minor'])

    def __parse_header_pre_request(self, method: dict) -> str:
        http_method = method['name']
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        pure_virtual = ' = 0' if http_method == 'POST' or http_method == 'PUT' else ''
        request = 'virtual Reply *on{}Request(/* HTTP {} */){};'.format(method_name, http_method, pure_virtual)
        return request

    def __parse_header_method_success(self, method: dict) -> str:
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        return 'virtual QJSValueList on{}Success(const QByteArray &data);'.format(method_name)

    def __parse_header_method_error(self, method: dict) -> str:
        method_name = self.__cleanup_method_name(method['id'])
        method_name = method_name[0].capitalize() + method_name[1:]
        return 'virtual QJSValueList on{}Error(const QByteArray &data);'.format(method_name)

    @staticmethod
    def __translate_type(parameter_type: str) -> str:
        if parameter_type == 'string':
            return 'const QString &'
        elif parameter_type == 'boolean':
            return 'const bool '
        elif parameter_type == 'long':
            return 'const long '
        elif parameter_type == 'int':
            return 'const int '
        else:
            raise UnsupportedParameterTypeException(parameter_type)

    @staticmethod
    def __cleanup_file_name(name: str) -> str:
        return name.replace('-', '').lower()

    @staticmethod
    def __cleanup_class_name(name: str) -> str:
        name = name.capitalize()
        known_words = ['option', 'properties', 'field', 'user', 'picker', 'type', 'link', 'role',
                       'validator', 'mission', 'preference', 'self', 'category', 'validate', 'index',
                       'level', 'info', 'avatar', 'security', 'scheme']
        for word in known_words:
            name = name.replace(word, word.capitalize())
        return name

    @staticmethod
    def __cleanup_method_name(name: str) -> str:
        known_words = [{'delete': 'delete_'}]
        name = (name[0].lower() + name[1:]).replace('-', '')
        for word in known_words:
            for word_key, word_value in word.items():
                if name == word_key:
                    name = name.replace(word_key, word_value)
        return name

    @staticmethod
    def __cleanup_parameter_name(name: str) -> str:
        return (name[0].lower() + name[1:]).replace('-', '')
