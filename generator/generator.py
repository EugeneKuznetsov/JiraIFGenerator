import logging as log
from argparse import ArgumentParser
from pathlib import Path
from common.errors import GeneratorException
from parser.jirawadl import ResourceParser


def main(wadl_file: str, output_dir: str):
    validate_args(wadl_file, output_dir)
    endpoints = ResourceParser(wadl_file).get_endpoints()
    for endpoint in endpoints:
        for sub_endpoint in endpoint['sub_resources']:
            print(sub_endpoint)


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
