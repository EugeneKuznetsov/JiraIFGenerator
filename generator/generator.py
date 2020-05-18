import logging as log
from argparse import ArgumentParser
from pathlib import Path
from common.errors import GeneratorException
from parser.jirawadl import ResourceParser
from parser.resourcebundle import Bundle
from parser.endpoint import Endpoint


class EndpointGenerator:
    __output_dir: str
    __endpoint: Endpoint

    def __init__(self, endpoint: Endpoint, output_directory: str):
        self.__endpoint = endpoint
        self.__output_dir = output_directory + '/'

    def generate(self):
        endpoint = self.__endpoint
        with open(self.__output_dir + endpoint.header_filename, 'w') as header_file:
            header_file.write(endpoint.header_content)
        with open(self.__output_dir + endpoint.source_filename, 'w') as source_file:
            source_file.write(endpoint.source_content)


def main(wadl_file: str, output_dir: str):
    validate_args(wadl_file, output_dir)
    resources = ResourceParser(wadl_file).get_resources()
    endpoints = Bundle().pack(resources)
    for name, methods in endpoints.items():
        EndpointGenerator(Endpoint(name, methods, {'major': 0, 'minor': 2}), output_dir).generate()


def validate_args(wadl_file: str, output_dir: str):
    if Path(wadl_file).exists() is False:
        raise GeneratorException('WADL file {} does not exist'.format(wadl_file))
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    except OSError as err:
        raise GeneratorException('Could not create an output directory {}\n{}'.format(output_dir, err))


if __name__ == '__main__':
    parser = ArgumentParser(description='Jira REST API Endpoints interface generator for Jira QML extension module',
                            usage='%(prog)s input output')
    parser.add_argument('input', help='Absolute path to Jira REST API WADL document')
    parser.add_argument('output', help='Output directory for generated interfaces of endpoints')
    args = parser.parse_args()
    try:
        main(args.input, args.output)
    except GeneratorException as error:
        log.error('{}'.format(error))
        exit(error.code())
