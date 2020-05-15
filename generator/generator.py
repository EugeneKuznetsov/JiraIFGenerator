import logging as log
from argparse import ArgumentParser
from pathlib import Path


def main(wadl_file: str, output_dir: str):
    validate_args(wadl_file, output_dir)


def validate_args(wadl_file: str, output_dir: str):
    if Path(wadl_file).exists() is False:
        exit(1)
    try:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
    except OSError as err:
        log.error('Could not create an output directory {}\n   Error text: {}'.format(output_dir, err))
        exit(1)


if __name__ == '__main__':
    parser = ArgumentParser(description='Jira REST API Endpoints interface generator for Jira QML extension module',
                            usage='%(prog)s input output')
    parser.add_argument('input', help='Absolute path to Jira REST API WADL document')
    parser.add_argument('output', help='Output directory for generated interfaces of endpoints')
    args = parser.parse_args()
    main(args.input, args.output)
