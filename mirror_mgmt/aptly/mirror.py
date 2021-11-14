from .run import aptly_run


def run(command, **kwargs):
    return aptly_run(['mirror'] + command, **kwargs)


class Mirror:
    def __init__(self, name, **kwargs):
        self.name = name
        self.repository = kwargs.get('repository')
        self.distribution = kwargs.get('distribution')
        self.component = kwargs.get('component')

    @property
    def exists(self):
        return run(['show', self.name], check=False).returncode == 0

    def ensure_exists(self, repository=None, distribution=None, component=None, filters=None, extra_options=None):
        if not self.exists:
            self.create(
                repository or self.repository, distribution or self.distribution, component or self.component,
                filters, extra_options,
            )

    def create(self, repository, distribution, component, filters=None, extra_options=None):
        return run(list(filter(
            bool, ['create'] + (extra_options or []) + ([f'-filter={filters}'] if filters else []) + [
                self.name, repository, distribution, component,
            ]
        )))

    def update(self):
        run(['update', self.name])


def list_mirrors():
    return [Mirror(line) for line in run(['list', '-raw']).stdout.splitlines()]
