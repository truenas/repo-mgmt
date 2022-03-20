import logging

from .list import get_manifest_mirrors

logger = logging.getLogger(__name__)


def create_mirrors() -> None:
    logger.debug('Creating mirrors')
    for mirror in get_manifest_mirrors():
        if mirror.exists:
            logger.info('%r already exists, skipping creating it', mirror.resource_name)
        else:
            mirror.create()
            logger.info('Successfully created %r mirror', mirror.resource_name)
