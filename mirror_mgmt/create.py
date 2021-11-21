import logging

from .list import get_manifest_mirrors, get_manifest_repositories
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)


def common_create(repo_mirrors: list, object_type: str) -> None:
    for repo_mirror in repo_mirrors:
        if repo_mirror.exists:
            logger.info('%r already exists, skipping creating it', repo_mirror.name)
        else:
            repo_mirror.create()
            logger.info('Successfully created %r %s', repo_mirror.name, object_type)


def create_mirrors() -> None:
    manifest = get_manifest()
    logger.debug('Creating mirrors')
    logger.debug('Defined mirror suffix is %r', manifest['mirror_suffix'])
    common_create(get_manifest_mirrors(), 'mirror')


def create_repositories() -> None:
    logger.debug('Creating repositories')
    common_create(get_manifest_repositories(), 'repository')
