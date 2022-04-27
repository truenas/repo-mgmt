import logging
import typing

from .aptly.utils import drop_snapshot, get_all_published_snapshots, snapshot_is_published


logger = logging.getLogger(__name__)


def remove_dangling_snapshots(snapshots: list, published_snaps: typing.Optional[str] = None):
    published_snaps = published_snaps or get_all_published_snapshots()
    for snapshot_name in snapshots:
        if not snapshot_is_published(snapshot_name, published_snaps):
            logger.info('Removing %r snapshot', snapshot_name)
            drop_snapshot(snapshot_name)
