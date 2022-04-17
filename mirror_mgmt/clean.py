import logging

from .aptly.mirror import Mirror
from .aptly.resource import clean_database
from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def remove_snapshots_of_mirror(mirror: Mirror) -> None:
    logger.info('Removing snapshots of %r', mirror.name)
    for snapshot in mirror.get_snapshots():
        logger.info('Removing %r snapshot', snapshot.name)
        snapshot.delete()


def clean_mirrors() -> None:
    """
    How this needs to work out is in the following manner:
    1. Drop published snapshots of this mirror
    2. Drop snapshots created from this mirror
    3. Drop the mirror finally
    """
    logger.debug('Cleaning mirrors')
    for mirror in get_manifest_mirrors():
        if mirror.exists:
            remove_snapshots_of_mirror(mirror)
            logger.info('Removing %r mirror', mirror.name)
            mirror.drop()
        else:
            logger.info('%r mirror does not exist, skipping dropping it', mirror.name)

    logger.info('Cleaning aptly database')
    clean_database()
    logger.info('Successfully cleaned aptly database')
