import functools
import jsonschema
import yaml

from mirror_mgmt.exceptions import CallError, MissingManifest

from .paths import MANIFEST_PATH


MANIFEST_SCHEMA = {
    'type': 'object',
    'properties': {
        'release': {'type': 'string'},
        'gpg_key': {'type': 'string'},
        'publish_prefix_default': {'type': 'string'},
        'mirror_suffix': {'type': 'string'},
        'mirrors': {
            'type': 'array',
            'items': [{
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'url': {'type': 'string'},
                    'distribution': {'type': 'string'},
                    'gpg_key': {'type': 'string'},
                    'publish_prefix_override': {'type': 'string'},
                    'component': {'type': 'string'},
                    'filter': {'type': 'string'},
                    'extra_options': {
                        'type': 'array',
                        'items': [{'type': 'string'}]
                    },
                },
                'required': ['name', 'url', 'distribution', 'component']
            }],
        },
    },
    'required': [
        'release',
        'gpg_key',
        'publish_prefix_default',
        'mirror_suffix',
        'mirrors',
    ],
}


def get_manifest_str() -> str:
    try:
        with open(MANIFEST_PATH, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise MissingManifest()


@functools.cache
def get_manifest() -> dict:
    try:
        manifest = yaml.safe_load(get_manifest_str())
        # jsonschema.validate(manifest, MANIFEST_SCHEMA)
        # TODO: FIX json schema validation
        return manifest
    except yaml.YAMLError:
        raise CallError('Provided manifest has invalid format')
    except jsonschema.ValidationError as e:
        raise CallError(f'Provided manifest is invalid: {e}')


def get_release_code_name() -> str:
    return get_manifest()['release']
