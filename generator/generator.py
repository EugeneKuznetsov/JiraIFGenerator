import logging as log
from argparse import ArgumentParser
from pathlib import Path
from common.errors import GeneratorException
from parser.jirawadl import ResourceParser
from parser.resourcebundle import Bundle


def main(wadl_file: str, output_dir: str):
    validate_args(wadl_file, output_dir)
    resources = ResourceParser(wadl_file).get_resources()
    endpoints = Bundle().pack(resources)
    for i, endpoint in enumerate(endpoints.keys()):
        print('{}) {}'.format(i, endpoint))
        for method in endpoints[endpoint]:
            if method.get('doc'):
                print('\t\t{}'.format(method['doc'].replace('\n', '')))
            print('\t[{}] {} -> {}'.format(method['name'], method['id'], method['path']))
            if method.get('parameters'):
                for parameter in method['parameters']:
                    print('\t\tQuery Parameter: {}'.format(parameter))
            if method.get('request') and method['request'].get('parameters'):
                for parameter in method['request']['parameters']:
                    print('\t\tRequest Parameter: {}'.format(parameter))
        print()


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
