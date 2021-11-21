import subprocess

from typing_extensions import ParamSpec

from mirror_mgmt.utils.manifest import get_manifest

from .run import aptly_run

P = ParamSpec('P')


class Resource:

    RESOURCE_NAME = NotImplementedError

    def __init__(self, name: str, **kwargs: P.kwargs):
        self.name = name
        self.distribution = kwargs.get('distribution')
        self.publish_prefix_override = kwargs.get('publish_prefix_override')

    def run(self, command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
        return aptly_run([self.RESOURCE_NAME] + command, **kwargs)

    @property
    def resource_name(self) -> str:
        return f'{self.name}-{get_manifest()["release"]}'

    @property
    def exists(self) -> bool:
        return self.run(['show', self.resource_name], check=False, log=False).returncode == 0

    def create(self) -> subprocess.CompletedProcess:
        raise NotImplementedError

    def update(self) -> None:
        raise NotImplementedError
