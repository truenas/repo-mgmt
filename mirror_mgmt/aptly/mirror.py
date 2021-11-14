from .run import aptly_run


def run(command, **kwargs):
    return aptly_run(['mirror'] + command, **kwargs)


class Mirror:
    def __init__(self, name):
        self.name = name

    @property
    def exists(self):
        return run(['show', self.name], check=False).returncode == 0


def list_mirrors():
    return [Mirror(line) for line in run(['list', '-raw']).stdout.splitlines()]
