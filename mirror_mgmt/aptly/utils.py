from .run import aptly_run


def get_all_snapshots() -> str:
    return aptly_run(['snapshot', 'list'], log=False).stdout
