import subprocess

from typing import ParamSpec

from .run import aptly_run

P = ParamSpec('P')


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

    def publish(self, distribution, endpoint, gpg_key) -> None:
        pass
