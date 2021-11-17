import subprocess

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

    @property
    def exists(self) -> bool:
        return run(['show', self.name], check=False).returncode == 0

    def ensure_exists(
        self, repository: Optional[str] = None, distribution: Optional[str] = None, component: Optional[str] = None,
        filters: Optional[str] = None, extra_options: Optional[list] = None,
    ) -> None:
        if not self.exists:
            self.create(
                repository or self.repository, distribution or self.distribution, component or self.component,
                filters, extra_options,
            )

    def create(
        self, repository: str, distribution: str, component: str, filters: Optional[str] = None,
        extra_options: Optional[list] = None
    ) -> subprocess.CompletedProcess:
        return run(list(filter(
            bool, ['create'] + (extra_options or []) + ([f'-filter={filters}'] if filters else []) + [
                self.name, repository, distribution, component,
            ]
        )))

    def update(self) -> None:
        run(['update', self.name])


def list_mirrors() -> list:
    return [Mirror(line) for line in run(['list', '-raw']).stdout.splitlines()]
