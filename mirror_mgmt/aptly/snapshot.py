import os.path

from mirror_mgmt.utils.manifest import get_manifest
from mirror_mgmt.exceptions import CallError

from typing_extensions import ParamSpec

from .resource import Resource
from .run import aptly_run

P = ParamSpec('P')


class Snapshot(Resource):

    RESOURCE_NAME = 'snapshot'

    def __init__(self, name: str, parent_resource: Resource, **kwargs: P.kwargs):
        super().__init__(name, **kwargs)
        self.parent_resource = parent_resource

    @property
    def resource_name(self) -> str:
        return self.name

    @property
    def endpoint(self) -> str:
        return f'filesystem:truenas:{self.publish_prefix}'

    @property
    def publish_prefix(self) -> str:
        return self.publish_prefix_override or os.path.join(
            get_manifest()['publish_prefix_default'], self.parent_resource.name
        )

    def create(self) -> None:
        self.run([
            'create', self.resource_name, 'from',
            self.parent_resource.RESOURCE_NAME, self.parent_resource.resource_name
        ])

    def delete(self) -> None:
        self.run(['drop', self.resource_name], log=False)

    @property
    def snap_distribution(self) -> str:
        return 'bullseye' if self.distribution == '/' else self.distribution

    def publish(self, gpg_key: str) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when publishing snapshot')

        aptly_run([
            'publish', 'snapshot', f'-distribution="{self.snap_distribution}"', f'-gpg-key={gpg_key}',
            self.resource_name, self.endpoint,
        ])

    def drop_published_snapshot(self) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when removing published snapshot')

        aptly_run(['publish', 'drop', self.snap_distribution, self.endpoint], check=False, log=False)
