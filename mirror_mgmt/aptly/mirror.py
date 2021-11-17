import subprocess

from mirror_mgmt.exceptions import CallError

from typing import Optional, ParamSpec

from .run import aptly_run

P = ParamSpec('P')


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['mirror'] + command, **kwargs)


class Mirror:
    def __init__(self, name: str, **kwargs: P.kwargs):
        self.name = name
        self.repository = kwargs.get('repository')
        self.distribution = kwargs.get('distribution')
        self.component = kwargs.get('component')
        self.extra_options = kwargs.get('extra_options')
        self.filter = kwargs.get('filter')

    def update_configuration(self, mirror_options: dict) -> None:
        self.repository = mirror_options['url']
        self.distribution = mirror_options['distribution']
        self.component = mirror_options['component']
        self.extra_options = mirror_options.get('extra_options', [])
        self.filter = mirror_options.get('filter')

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False).returncode == 0

    def create(self, gpg_key: Optional[str] = None) -> subprocess.CompletedProcess:
        missing = [k for k in ('repository', 'distribution', 'name') if not getattr(self, k)]
        if missing:
            raise CallError(f'{", ".join(missing)!r} must be specified before attempting to create mirror')

        if gpg_key:
            cp = subprocess.Popen(
                ['gpg', '--no-default-keyring', '--keyring', 'trustedkeys.gpg', '--import'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
            )
            stdout, stderr = cp.communicate(input=gpg_key.encode())
            if cp.returncode:
                raise CallError(f'Failed to add gpg key for {self.repository!r}: {stderr.decode(errors="ignore")}')

        return run(list(filter(
            bool, ['create'] + (self.extra_options or []) + ([f'-filter={self.filter}'] if self.filter else []) + [
                self.name, self.repository, self.distribution, self.component,
            ]
        )))

    def update(self) -> None:
        run(['update', self.name])


def list_mirrors() -> list:
    return [Mirror(line) for line in run(['list', '-raw']).stdout.splitlines()]
