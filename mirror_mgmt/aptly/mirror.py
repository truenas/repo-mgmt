import re
import subprocess

from mirror_mgmt.exceptions import CallError

from typing import Optional
from typing_extensions import ParamSpec

from .resource import Resource
from .snapshot import Snapshot
from .utils import get_all_snapshots

P = ParamSpec('P')
RE_URI = re.compile(r'Archive Root URL:\s*(.*)')


class Mirror(Resource):

    RESOURCE_NAME = 'mirror'

    def __init__(self, name: str, **kwargs: P.kwargs):
        super().__init__(name, **kwargs)
        self.repository = kwargs.get('url')
        self.component = kwargs.get('component', [])
        self.extra_options = kwargs.get('extra_options', [])
        self.filter = kwargs.get('filter')
        self.gpg_key = kwargs.get('gpg_key')

    def create_snapshot(self, snapshot_name: Optional[str] = None) -> Snapshot:
        snap = self.get_snap_object(snapshot_name)
        if snap.exists:
            snap.delete()

        snap.create()
        return snap

    def drop(self):
        self.run(['drop', '-force', self.resource_name])

    def get_snap_object(self, snapshot_name: str) -> Snapshot:
        return Snapshot(
            snapshot_name, self, distribution=self.distribution, publish_prefix_override=self.publish_prefix_override,
        )

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
                self.resource_name, self.repository, self.distribution,
            ] + self.component
        )))

    def update(self) -> None:
        self.run(['update', self.resource_name])

    def needs_to_be_created(self) -> bool:
        show_details = self.run(['show', self.resource_name], check=False, log=False)
        if show_details.returncode != 0:
            return True

        repository = RE_URI.findall(show_details.stdout)
        return not repository or repository[0].rstrip('/') != self.repository

    def get_snapshots(self) -> list:
        return [
            self.get_snap_object(snapshot_name)
            for snapshot_name in re.findall(
                fr'.*\[(.*)\].* Snapshot from mirror\s*\[{self.resource_name}\].*', get_all_snapshots()
            )
        ]
