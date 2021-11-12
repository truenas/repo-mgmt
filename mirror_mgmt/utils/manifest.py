import functools
import yaml

from mirror_mgmt.exceptions import CallError, MissingManifest

from .paths import MANIFEST_PATH


def get_manifest_str():
    try:
        with open(MANIFEST_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise MissingManifest()


@functools.cache
def get_manifest():
    # TODO: Validate provided manifest
    try:
        manifest = yaml.safe_load(get_manifest_str())
        return manifest
    except yaml.YAMLError:
        raise CallError('Provided manifest has invalid format')


def get_release_code_name():
    return get_manifest()['release']
