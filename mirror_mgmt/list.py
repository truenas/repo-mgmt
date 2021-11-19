from .aptly.mirror import Mirror
from .utils.manifest import get_manifest


def get_manifest_mirrors() -> list:
    return [Mirror(**m) for m in get_manifest()['mirrors']]