import logging

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def create_mirrors() -> None:
    logger.info('Updating mirrors')

    for mirror in get_manifest_mirrors():
        if not mirror.exists:
            logger.debug('Creating %r mirror', mirror.name)
            mirror.create()

        logging.debug('Updating %r mirror', mirror.name)
        mirror.update()
        logging.debug('Updated %r mirror', mirror.name)
