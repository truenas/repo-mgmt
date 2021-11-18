import logging

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def update_mirrors() -> None:
    logger.debug('Updating mirrors')

    for mirror in get_manifest_mirrors():
        if not mirror.exists:
            logger.info('Creating %r mirror', mirror.name)
            mirror.create()

        logging.info('Updating %r mirror', mirror.name)
        mirror.update()
        logging.info('Updated %r mirror', mirror.name)
