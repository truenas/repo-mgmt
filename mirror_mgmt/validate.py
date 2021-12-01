import os
import logging
import shutil

from .exceptions import CallError
from .utils.manifest import get_manifest


logger = logging.getLogger(__name__)

WANTED_PACKAGES = {
    'gpg1',
    'aptly',
    'git',
    'zfs',
}


def retrieve_missing_packages():
    return {pkg for pkg in WANTED_PACKAGES if not shutil.which(pkg)}


def validate_system_state():
    if os.geteuid() != 0:
        raise CallError('Must be run as root (or using sudo)!')

    missing_packages = retrieve_missing_packages()
    if missing_packages:
        raise CallError(f'{", ".join(missing_packages)!r} packages are missing and are required in order to proceed')


def validate(system_state_flag=True, manifest_flag=True):
    if system_state_flag:
        validate_system_state()
        logger.debug('System state Validated')
    if manifest_flag:
        get_manifest()
        logger.debug('Manifest Validated')
