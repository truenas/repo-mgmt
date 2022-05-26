import logging

from mirror_mgmt.exceptions import CallError

from .list import get_manifest_mirrors


logger = logging.getLogger(__name__)


def update_mirrors(mirrors_to_update: list) -> None:
    logger.debug('Updating mirrors')
    mirrors = {m.resource_name: m for m in get_manifest_mirrors()}
    if set(mirrors_to_update) - set(mirrors):
        raise CallError(
            f'{", ".join(set(mirrors_to_update) - set(mirrors))!r} mirrors are not specified in the manifest'
        )

    for mirror in ([mirrors[m] for m in mirrors_to_update] if mirrors_to_update else mirrors.values()):
        if mirror.needs_to_be_created():
            if mirror.exists:
                logger.info('Removing %r mirror as it needs to be re-created', mirror.resource_name)
                mirror.drop()

            logger.info('Creating %r mirror', mirror.resource_name)
            mirror.create()

        logger.info('Updating %r mirror', mirror.resource_name)
        mirror.update()
        logger.info('Updated %r mirror', mirror.resource_name)
