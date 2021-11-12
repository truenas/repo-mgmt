import argparse
import coloredlogs
import logging
import sys


logger = logging.getLogger('mirror_mgmt')


def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', force=True)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(handler)
    logger.propagate = False
    if sys.stdout.isatty():
        coloredlogs.install(logging.DEBUG, fmt='[%(asctime)s] %(message)s', logger=logger)


def validate_config():
    pass


def main():
    setup_logging()
    parser = argparse.ArgumentParser(prog='mirror_mgmt')
    subparsers = parser.add_subparsers(help='sub-command help', dest='action')

    subparsers.add_parser('create_mirror', help='Create new mirror from the configuration provided')

    args = parser.parse_args()
    if args.action == 'create_mirror':
        pass
    else:
        parser.print_help()
