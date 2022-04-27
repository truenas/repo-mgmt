import re

from .run import aptly_run


def get_all_snapshots(get_raw: bool = False) -> str:
    return aptly_run(['snapshot', 'list'] + (['-raw'] if get_raw else []), log=False).stdout


def get_all_published_snapshots() -> str:
    return aptly_run(['publish', 'list'], log=False).stdout


def snapshot_is_published(snap_name: str, published_snapshots: str) -> bool:
    return bool(
        re.findall(fr'publishes\s*\{{.*:\s*\[{snap_name}\]:\s*Snapshot from.*', published_snapshots)
    )


def drop_snapshot(snap_name: str) -> None:
    aptly_run(['snapshot', 'drop', snap_name], log=False)
