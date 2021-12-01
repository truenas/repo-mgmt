from .run import run


def zfs_snapshot(dataset: str, snap_name: str) -> None:
    run(['zfs', 'snapshot', '-r', f'{dataset}@{snap_name}'], log=False)
