import subprocess

from mirror_mgmt.exceptions import CallError

from typing_extensions import ParamSpec

from .run import aptly_run

P = ParamSpec('P')


def get_endpoint(prefix: str) -> str:
    return f'filesystem:truenas:{prefix}'


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['snapshot'] + command, **kwargs)


class Snapshot:
    def __init__(self, name: str, **kwargs: P.kwargs):
        self.name = name
        self.update_configuration(kwargs)

    def update_configuration(self, options: dict) -> None:
        self.distribution = options.get('distribution')

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False, log=False).returncode == 0

    def create(self, mirror) -> None:
        run(['create', self.name, 'from', 'mirror', mirror])

    def publish(self, prefix: str, gpg_key: str) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when publishing snapshot')

        aptly_run([
            'publish', 'snapshot', f'-distribution="{self.distribution}"', f'-gpg-key={gpg_key}',
            self.name, get_endpoint(prefix),
        ])

    def drop_published_snapshot(self, prefix: str) -> None:
        if not self.distribution:
            raise CallError('Distribution must be specified when removing published snapshot')

        aptly_run(['publish', 'drop', self.distribution, get_endpoint(prefix)], check=False)


def list_snapshots():
    return [Snapshot(line) for line in run(['list', '-raw']).stdout.splitlines()]
