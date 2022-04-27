import argparse
import coloredlogs
import logging
import sys

from .clean import clean_dangling_snapshots, clean_mirrors
from .create import create_mirrors
from .snapshot import (
    backup_aptly_dataset, create_snapshots_of_mirrors, publish_snapshots_of_mirrors,
)
from .update import update_mirrors
from .validate import validate


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


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(prog='mirror_mgmt')
    subparsers = parser.add_subparsers(help='sub-command help', dest='action')

    subparsers.add_parser('clean_mirrors', help='Drop mirrors from the configuration provided')
    subparsers.add_parser('clean_dangling', help='Drop unpublished aptly snapshots from the configuration provided')
    subparsers.add_parser(
        'create_mirrors', help='fCreate new mirrors from the configuration provided'
    )
    subparsers.add_parser('update_mirrors', help='Update mirrors specified in the manifest')
    snapshot_parser = subparsers.add_parser(
        'create_mirrors_snapshots', help='Create snapshots of mirrors specified in the manifest'
    )
    snapshot_parser.add_argument(
        '--snapshot-suffix', help='Specify suffix to use for creating snapshot from mirror'
    )
    snapshot_parser.add_argument(
        '--publish-snapshot', '-ps', help='Publish snapshot', default=False, action='store_true'
    )

    subparsers.add_parser('backup', help='Backup aptly mirror dataset')
    validate_parser = subparsers.add_parser(
        'validate', help='Validate TrueNAS Scale mirror management manifest and system state'
    )
    for action in ('manifest', 'system_state'):
        validate_parser.add_argument(f'--validate-{action}', dest=action, action='store_true')
        validate_parser.add_argument(f'--no-validate-{action}', dest=action, action='store_false')
        validate_parser.set_defaults(**{action: True})

    args = parser.parse_args()
    if args.action == 'backup':
        backup_aptly_dataset()
    elif args.action == 'clean_mirrors':
        clean_mirrors()
    elif args.action == 'clean_dangling':
        clean_dangling_snapshots()
    elif args.action == 'validate':
        validate(args.system_state, args.manifest)
    elif args.action == 'create_mirrors':
        validate()
        create_mirrors()
    elif args.action == 'update_mirrors':
        validate()
        update_mirrors()
        clean_dangling_snapshots()
    elif args.action == 'create_mirrors_snapshots':
        validate()
        snapshots = create_snapshots_of_mirrors(args.snapshot_suffix)
        if args.publish_snapshot:
            publish_snapshots_of_mirrors(snapshots)
        clean_dangling_snapshots()
    else:
        parser.print_help()
