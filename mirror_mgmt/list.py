from .aptly.mirror import Mirror
from .aptly.utils import get_all_snapshots
from .utils.manifest import get_manifest


def get_manifest_mirrors() -> list:
    return [Mirror(**m) for m in get_manifest()['mirrors']]


def get_snapshots() -> list:
    return [s for s in filter(bool, map(str.strip, get_all_snapshots(True).split('\n')))]
