import logging

from datetime import datetime

from .list import get_manifest_mirrors, get_manifest_repositories
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)


def common_create_snapshots(repo_mirrors: list, object_type: str, snapshot_suffix: str) -> list:
    snapshots = []
    logger.debug('Creating snapshots...')
    for repo_mirror in repo_mirrors:
        snap_name = f'{repo_mirror.resource_name}-{datetime.today().strftime("%Y-%m-%d")}-{snapshot_suffix}'
        logger.info('Creating %r snapshot of %r %s', snap_name, repo_mirror.name, object_type)
        snapshots.append(repo_mirror.create_snapshot(snap_name))
    return snapshots


def common_publish_snapshots(snapshots: list, object_type: str) -> None:
    logger.info('Publishing snapshots...')
    for snapshot in snapshots:
        logger.debug(
            'Publishing %r snapshot of %r %s using endpoint %r', snapshot.name,
            snapshot.parent_resource_name, object_type, snapshot.endpoint
        )
        snapshot.drop_published_snapshot()
        snapshot.publish(get_manifest()['gpg_key'])


def create_snapshots_of_mirrors(snapshot_suffix: str) -> list:
    return common_create_snapshots(get_manifest_mirrors(), 'mirror', snapshot_suffix)


def publish_snapshots_of_mirrors(snapshots: list) -> None:
    common_publish_snapshots(snapshots, 'mirror')


def create_snapshots_of_repositories(snapshot_suffix: str) -> list:
    return common_create_snapshots(get_manifest_repositories(), 'repository', snapshot_suffix)


def publish_snapshots_of_repositories(snapshots: list) -> None:
    common_publish_snapshots(snapshots, 'repository')
