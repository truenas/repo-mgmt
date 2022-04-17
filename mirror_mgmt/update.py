import logging

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def update_mirrors() -> None:
    logger.debug('Updating mirrors')
    for mirror in get_manifest_mirrors():
        if mirror.needs_to_be_created():
            if mirror.exists:
                logger.info('Removing %r mirror as it needs to be re-created', mirror.resource_name)
                mirror.drop()

            logger.info('Creating %r mirror', mirror.resource_name)
            mirror.create()

        logger.info('Updating %r mirror', mirror.resource_name)
        mirror.update()
        logger.info('Updated %r mirror', mirror.resource_name)
