import subprocess

from typing import ParamSpec

from mirror_mgmt.utils.paths import APTLY_CONF
from mirror_mgmt.utils.run import run

P = ParamSpec('P')


def aptly_run(command: list, **kwargs: P.kwargs) -> subprocess.CompletedProcess:
    return run(['aptly', '-config', APTLY_CONF] + command, **kwargs)
