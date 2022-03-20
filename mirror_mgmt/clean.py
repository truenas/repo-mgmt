import logging

from .aptly.resource import clean_database
from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def clean_mirrors() -> None:
    logger.debug('Cleaning mirrors')
    for mirror in get_manifest_mirrors():
        if mirror.exists:
            logger.info('Removing %r mirror', mirror.name)
            mirror.drop()
        else:
            logger.info('%r mirror does not exist, skipping dropping it', mirror.name)

    logger.info('Cleaning aptly database')
    clean_database()
    logger.info('Successfully cleaned aptly database')
