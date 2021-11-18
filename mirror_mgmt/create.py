import logging

from .list import get_manifest_mirrors
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)


def create_mirrors() -> None:
    manifest = get_manifest()
    logger.info('Creating mirrors')
    logger.info('Defined mirror suffix is %r', manifest['mirror_suffix'])

    for mirror in get_manifest_mirrors():
        if mirror.exists:
            logger.debug('%r already exists, skipping creating it', mirror.name)
        else:
            mirror.create()
            logger.debug('Successfully created %r mirror', mirror.name)
