import argparse
import coloredlogs
import logging
import sys

from .create import create_mirrors


logger = logging.getLogger('mirror_mgmt')


def setup_logging() -> None:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(message)s', force=True)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(handler)
    logger.propagate = False
    if sys.stdout.isatty():
        coloredlogs.install(logging.DEBUG, fmt='[%(asctime)s] %(message)s', logger=logger)


def validate_config() -> None:
    pass


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(prog='mirror_mgmt')
    subparsers = parser.add_subparsers(help='sub-command help', dest='action')

    subparsers.add_parser('create_mirrors', help='Create new mirrors from the configuration provided')
    subparsers.add_parser('update_mirrors', help='Update mirrors specified in the manifest')

    args = parser.parse_args()
    if args.action == 'create_mirrors':
        create_mirrors()
    elif args.action == 'update_mirrors':
        pass
    else:
        parser.print_help()
