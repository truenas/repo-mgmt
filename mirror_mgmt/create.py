import logging

from .aptly.mirror import Mirror
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)


def get_manifest_mirrors() -> list:
    mirror_suffix = get_manifest()['mirror_suffix']
    return [
        Mirror(**m) for m in map(lambda m: m.update({'name': f'{m["name"]}{mirror_suffix}'}), get_manifest()['mirrors'])
    ]


def create_mirrors() -> None:
    manifest = get_manifest()
    logger.info('Creating mirrors')
    logger.info('Defined mirror suffix is %r', manifest['mirror_suffix'])

    for mirror in get_manifest_mirrors():
        if mirror.exists:
            logger.debug(f'%r already exists, skipping creating it', mirror.name)
        else:
            mirror.create()
            logger.debug('Successfully created %r mirror', mirror.name)
