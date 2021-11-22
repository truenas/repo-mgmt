import subprocess

from mirror_mgmt.exceptions import CallError

from typing import Optional
from typing_extensions import ParamSpec

from .resource import Resource
from .run import aptly_run
from .snapshot import Snapshot

P = ParamSpec('P')


class RepositoryBase(Resource):

    def create_snapshot(self, snapshot_name: Optional[str] = None) -> Snapshot:
        snap = Snapshot(
            snapshot_name, self, distribution=self.distribution,
            publish_prefix_override=self.publish_prefix_override,
        )
        if snap.exists:
            snap.delete()

        snap.create()
        return snap

    def drop(self):
        self.run(['drop', '-force', self.resource_name])


class Repository(RepositoryBase):

    RESOURCE_NAME = 'repo'

    def __init__(self, name: str, **kwargs: P.kwargs):
        super().__init__(name, **kwargs)
        self.package_directory = kwargs.get('package_directory')

    def create(self) -> subprocess.CompletedProcess:
        missing = [k for k in ('package_directory', 'distribution', 'name') if not getattr(self, k)]
        if missing:
            raise CallError(f'{", ".join(missing)!r} must be specified before attempting to create repository')

        return self.run(['create', self.name])

    def update(self) -> None:
        self.run(['add', '-remove-files', '-force-replace', self.name, self.package_directory])
