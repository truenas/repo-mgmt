import argparse
import coloredlogs
import logging
import sys

from .clean import clean_mirrors, clean_repositories
from .create import create_mirrors, create_repositories
from .snapshot import (
    create_snapshots_of_mirrors, create_snapshots_of_repositories,
    publish_snapshots_of_mirrors, publish_snapshots_of_repositories,
)
from .update import update_mirrors, update_repositories
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

    for object_singular, object_plural in (('mirror', 'mirrors'), ('repository', 'repositories')):
        subparsers.add_parser(
            f'clean_{object_plural}', help=f'Drop {object_plural} from the configuration provided'
        )
        subparsers.add_parser(
            f'create_{object_plural}', help=f'fCreate new {object_plural} from the configuration provided'
        )
        subparsers.add_parser(f'update_{object_plural}', help=f'Update {object_plural} specified in the manifest')
        snapshot_parser = subparsers.add_parser(
            f'create_{object_plural}_snapshots', help=f'Create snapshots of {object_plural} specified in the manifest'
        )
        snapshot_parser.add_argument(
            '--snapshot-suffix', help=f'Specify suffix to use for creating snapshot from {object_singular}'
        )
        snapshot_parser.add_argument(
            '--publish-snapshot', '-ps', help='Publish snapshot', default=False, action='store_true'
        )

    validate_parser = subparsers.add_parser(
        'validate', help='Validate TrueNAS Scale mirror management manifest and system state'
    )
    for action in ('manifest', 'system_state'):
        validate_parser.add_argument(f'--validate-{action}', dest=action, action='store_true')
        validate_parser.add_argument(f'--no-validate-{action}', dest=action, action='store_false')
        validate_parser.set_defaults(**{action: True})

    args = parser.parse_args()
    if args.action == 'clean_mirrors':
        clean_mirrors()
    elif args.action == 'clean_repositories':
        clean_repositories()
    elif args.action == 'validate':
        validate(args.system_state, args.manifest)
    elif args.action == 'create_mirrors':
        validate()
        create_mirrors()
    elif args.action == 'create_repositories':
        validate()
        create_repositories()
    elif args.action == 'update_mirrors':
        validate()
        update_mirrors()
    elif args.action == 'update_repositories':
        validate()
        update_repositories()
    elif args.action == 'create_mirrors_snapshots':
        validate()
        snapshots = create_snapshots_of_mirrors(args.snapshot_suffix)
        if args.publish_snapshot:
            publish_snapshots_of_mirrors(snapshots)
    elif args.action == 'create_repositories_snapshots':
        validate()
        snapshots = create_snapshots_of_repositories(args.snapshot_suffix)
        if args.publish_snapshot:
            publish_snapshots_of_repositories(snapshots)
    else:
        parser.print_help()
