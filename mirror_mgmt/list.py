from .aptly.mirror import Mirror
from .utils.manifest import get_manifest


def get_manifest_mirrors() -> list:
    mirror_suffix = get_manifest()['mirror_suffix']
    mirrors = []
    for mirror in get_manifest()['mirrors']:
        mirror['name'] = f'{mirror["name"]}{mirror_suffix}'
        mirrors.append(Mirror(**mirror))
    return mirrors
    return [
        Mirror(**m) for m in map(lambda m: m.update({'name': f'{m["name"]}{mirror_suffix}'}), get_manifest()['mirrors'])
    ]
