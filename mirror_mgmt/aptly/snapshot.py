import os.path
import subprocess

from mirror_mgmt.utils.manifest import get_manifest
from mirror_mgmt.exceptions import CallError

from typing_extensions import ParamSpec

from .run import aptly_run

P = ParamSpec('P')


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['snapshot'] + command, **kwargs)


class Snapshot:
    def __init__(self, name: str, mirror_name: str, **kwargs: P.kwargs):
        self.name = name
        self.mirror_name = mirror_name
        self.update_configuration(kwargs)

    def update_configuration(self, options: dict) -> None:
        self.distribution = options.get('distribution')
        self.publish_prefix_override = options.get('publish_prefix_override')

    @property
    def endpoint(self) -> str:
        return f'filesystem:truenas:{self.publish_prefix}'

    @property
    def publish_prefix(self) -> str:
        return self.publish_prefix_override or os.path.join(get_manifest()['publish_prefix_default'], self.mirror_name)

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False, log=False).returncode == 0

    def create(self) -> None:
        run(['create', self.name, 'from', 'mirror', self.mirror_name])

    def delete(self) -> None:
        run(['drop', self.name], log=False)

    @property
    def snap_distribution(self) -> str:
        return 'bullseye' if self.distribution == '/' else self.distribution

    def publish(self, gpg_key: str) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when publishing snapshot')

        aptly_run([
            'publish', 'snapshot', f'-distribution="{self.snap_distribution}"', f'-gpg-key={gpg_key}',
            self.name, self.endpoint,
        ])

    def drop_published_snapshot(self) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when removing published snapshot')

        aptly_run(['publish', 'drop', self.snap_distribution, self.endpoint], check=False, log=False)
