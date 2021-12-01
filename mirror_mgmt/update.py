import logging

from .list import get_manifest_mirrors, get_manifest_repositories


logger = logging.getLogger(__name__)


def common_update(repo_mirrors: list, object_type: str):
    for repo_mirror in repo_mirrors:
        if not repo_mirror.exists:
            logger.info('Creating %r %s', repo_mirror.resource_name, object_type)
            repo_mirror.create()

        logger.info('Updating %r %s', repo_mirror.resource_name, object_type)
        repo_mirror.update()
        logger.info('Updated %r %s', repo_mirror.resource_name, object_type)


def update_mirrors() -> None:
    logger.debug('Updating mirrors')
    common_update(get_manifest_mirrors(), 'mirror')


def update_repositories() -> None:
    logger.debug('Updating repositories')
    common_update(get_manifest_repositories(), 'repository')
