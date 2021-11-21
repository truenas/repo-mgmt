import subprocess

from mirror_mgmt.exceptions import CallError

from typing import Optional
from typing_extensions import ParamSpec

from .run import aptly_run
from .snapshot import Snapshot

P = ParamSpec('P')


def run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return aptly_run(['repo'] + command, **kwargs)


class Repository:
    def __init__(self, name: str, **kwargs: P.kwargs):
        self.name = name
        self.update_configuration(kwargs)

    def update_configuration(self, mirror_options: dict) -> None:
        self.distribution = mirror_options.get('distribution')
        self.package_directory = mirror_options.get('package_directory')
        self.publish_prefix_override = mirror_options.get('publish_prefix_override')

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False, log=False).returncode == 0

    def create_snapshot(self, snapshot_name: Optional[str] = None) -> Snapshot:
        snap = Snapshot(
            snapshot_name, self.name, distribution=self.distribution,
            publish_prefix_override=self.publish_prefix_override,
        )
        if snap.exists:
            snap.delete()

        snap.create()
        return snap

    def create(self) -> subprocess.CompletedProcess:
        missing = [k for k in ('package_directory', 'distribution', 'name') if not getattr(self, k)]
        if missing:
            raise CallError(f'{", ".join(missing)!r} must be specified before attempting to create repository')

        return run(['create', self.name])

    def update(self) -> None:
        run(['add', '-remove-files', '-force-replace', self.name, self.package_directory])
