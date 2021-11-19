import logging

from datetime import datetime

from .list import get_manifest_mirrors
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)


def create_snapshots(snapshot_suffix: str) -> list:
    snapshots = []
    logger.debug('Creating snapshots...')
    for mirror in get_manifest_mirrors():
        snap_name = f'{mirror.name}-{datetime.today().strftime("%Y-%m-%d")}-{snapshot_suffix}'
        logger.info('Creating %r snapshot of %r mirror', snap_name, mirror.name)
        snapshots.append(mirror.create_snapshot(snap_name))
    return snapshots


def publish_snapshots(snapshots: list):
    logger.info('Publishing snapshots...')
    for snapshot in snapshots:
        logger.debug(
            'Publishing %r snapshot of %r mirror using endpoint %r', snapshot.name,
            snapshot.mirror_name, snapshot.endpoint
        )
        snapshot.drop_published_snapshot()
        snapshot.publish(get_manifest()['gpg_key'])
