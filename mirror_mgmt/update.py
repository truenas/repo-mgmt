import logging

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def update_mirrors() -> None:
    logger.debug('Updating mirrors')
    for mirror in get_manifest_mirrors():
        if not mirror.needs_to_be_created():
            logger.info('Creating %r mirror', mirror.resource_name)
            mirror.create()

        logger.info('Updating %r mirror', mirror.resource_name)
        mirror.update()
        logger.info('Updated %r mirror', mirror.resource_name)
