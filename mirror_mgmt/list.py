from .aptly.mirror import Mirror
from .aptly.repository import Repository
from .utils.manifest import get_manifest


def get_manifest_mirrors() -> list:
    return [Mirror(**m) for m in get_manifest()['mirrors']]


def get_manifest_repositories() -> list:
    return [Repository(**r) for r in get_manifest().get('repositories', [])]
