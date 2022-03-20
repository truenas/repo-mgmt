import logging
import time

from datetime import datetime

from .list import get_manifest_mirrors
from .utils.manifest import get_manifest
from .utils.zfs import zfs_snapshot

logger = logging.getLogger(__name__)


def create_snapshots_of_mirrors(snapshot_suffix: str) -> list:
    snapshots = []
    logger.debug('Creating snapshots...')
    for mirror in get_manifest_mirrors():
        snap_name = f'{mirror.resource_name}-{datetime.today().strftime("%Y-%m-%d")}-{snapshot_suffix}'
        logger.info('Creating %r snapshot of %r mirror', snap_name, mirror.resource_name)
        snapshots.append(mirror.create_snapshot(snap_name))
    return snapshots


def publish_snapshots_of_mirrors(snapshots: list) -> None:
    logger.debug('Publishing snapshots...')
    for snapshot in snapshots:
        logger.info(
            'Publishing %r snapshot of %r mirror using endpoint %r', snapshot.name,
            snapshot.parent_resource.resource_name, snapshot.endpoint
        )
        snapshot.drop_published_snapshot()
        snapshot.publish(get_manifest()['gpg_key'])


def backup_aptly_dataset() -> None:
    zfs_snapshot(get_manifest()['aptly_dataset'], f'backup_aptly_dataset_{int(time.time())}')
