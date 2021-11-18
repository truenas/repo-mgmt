from .aptly.mirror import Mirror
from .utils.manifest import get_manifest


def get_manifest_mirrors() -> list:
    mirror_suffix = get_manifest()['mirror_suffix']
    return [
        Mirror(**m) for m in map(lambda m: m.update({'name': f'{m["name"]}{mirror_suffix}'}), get_manifest()['mirrors'])
    ]
