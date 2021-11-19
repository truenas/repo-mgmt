import subprocess

from mirror_mgmt.utils.manifest import get_manifest
from mirror_mgmt.exceptions import CallError

from datetime import datetime
from typing import Optional
from typing_extensions import ParamSpec

from .run import aptly_run
from .snapshot import Snapshot

P = ParamSpec('P')


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['mirror'] + command, **kwargs)


class Mirror:
    def __init__(self, name: str, **kwargs: P.kwargs):
        self.name = name
        self.update_configuration(kwargs)

    @property
    def mirror_name(self) -> str:
        return f'{self.name}{get_manifest()["mirror_suffix"]}'

    def update_configuration(self, mirror_options: dict) -> None:
        self.repository = mirror_options.get('url')
        self.distribution = mirror_options.get('distribution')
        self.component = mirror_options.get('component')
        self.extra_options = mirror_options.get('extra_options', [])
        self.filter = mirror_options.get('filter')
        self.gpg_key = mirror_options.get('gpg_key')
        self.publish_prefix_override = mirror_options.get('publish_prefix_override')
        if mirror_options.get('name'):
            self.name = mirror_options['name']

    @property
    def exists(self) -> bool:
        return run(['show', self.mirror_name], check=False, log=False).returncode == 0

    def create_snapshot(self, snapshot_suffix: Optional[str] = None) -> Snapshot:
        name = f'{self.name}-{datetime.today().strftime("%Y-%m-%d")}-{snapshot_suffix}'
        snap = Snapshot(
            name, self.mirror_name, distribution=self.distribution,
            publish_prefix_override=self.publish_prefix_override,
        )
        if snap.exists:
            snap.delete()

        snap.create()
        return snap

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

        return run(list(filter(
            bool, ['create'] + (self.extra_options or []) + ([f'-filter={self.filter}'] if self.filter else []) + [
                self.mirror_name, self.repository, self.distribution, self.component,
            ]
        )))

    def update(self) -> None:
        run(['update', self.mirror_name])