import logging

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def create_snapshots(snapshot_suffix: str) -> list:
    snapshots = []
    for mirror in get_manifest_mirrors():
        snapshots.append(mirror.create_snapshot(snapshot_suffix))
    return snapshots


def publish_snapshots(snapshots: list):
    for snapshot in snapshots:
        pass
