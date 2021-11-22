import logging

from .aptly.resource import clean_database
from .list import get_manifest_mirrors, get_manifest_repositories


logger = logging.getLogger(__name__)


def common_drop(repo_mirrors: list, object_type: str) -> None:
    for repo_mirror in repo_mirrors:
        if repo_mirror.exists:
            logger.info('Removing %r %s', repo_mirror.name, object_type)
            repo_mirror.drop()
        else:
            logger.info('%r %s does not exist, skipping dropping it', repo_mirror.name, object_type)

    logger.info('Cleaning aptly database')
    clean_database()
    logger.info('Successfully cleaned aptly database')


def clean_mirrors() -> None:
    logger.debug('Cleaning mirrors')
    common_drop(get_manifest_mirrors(), 'mirror')


def clean_repositories() -> None:
    logger.debug('Cleaning repositories')
    common_drop(get_manifest_repositories(), 'repository')
