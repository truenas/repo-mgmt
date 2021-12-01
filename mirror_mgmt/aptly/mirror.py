import subprocess

from mirror_mgmt.exceptions import CallError

from typing_extensions import ParamSpec

from .repository import RepositoryBase

P = ParamSpec('P')


class Mirror(RepositoryBase):

    RESOURCE_NAME = 'mirror'

    def __init__(self, name: str, **kwargs: P.kwargs):
        super().__init__(name, **kwargs)
        self.repository = kwargs.get('url')
        self.component = kwargs.get('component')
        self.extra_options = kwargs.get('extra_options', [])
        self.filter = kwargs.get('filter')
        self.gpg_key = kwargs.get('gpg_key')

    def create(self) -> subprocess.CompletedProcess:
        missing = [k for k in ('repository', 'distribution', 'name') if not getattr(self, k)]
        if missing:
            raise CallError(f'{", ".join(missing)!r} must be specified before attempting to create mirror')

        if self.gpg_key:
            cp = subprocess.Popen(
                ['gpg', '--no-default-keyring', '--keyring', 'trustedkeys.gpg', '--import'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
            )
            stdout, stderr = cp.communicate(input=self.gpg_key.encode())
            if cp.returncode:
                raise CallError(f'Failed to add gpg key for {self.repository!r}: {stderr.decode(errors="ignore")}')

        return self.run(list(filter(
            bool, ['create'] + (self.extra_options or []) + ([f'-filter={self.filter}'] if self.filter else []) + [
                self.resource_name, self.repository, self.distribution, self.component,
            ]
        )))

    def update(self) -> None:
        self.run(['update', self.resource_name])
