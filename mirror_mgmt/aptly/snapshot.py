import subprocess

from typing import ParamSpec

from .run import aptly_run

P = ParamSpec('P')


def get_endpoint(prefix: str) -> str:
    return f'filesystem:truenas:{prefix}'


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['snapshot'] + command, **kwargs)


class Snapshot:
    def __init__(self, name: str):
        self.name = name

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False).returncode == 0

    def create(self, mirror) -> None:
        run(['create', self.name, 'from', 'mirror', mirror])

    def publish(self, distribution: str, prefix: str, gpg_key: str) -> None:
        aptly_run([
            'publish', 'snapshot', f'-distribution="{distribution}"', f'-gpg-key={gpg_key}',
            self.name, get_endpoint(prefix),
        ])

    def drop_published_snapshot(self, distribution: str, prefix: str) -> None:
        aptly_run(['publish', 'drop', distribution, get_endpoint(prefix)], check=False)


def list_snapshots():
    return [Snapshot(line) for line in run(['list', '-raw']).stdout.splitlines()]
