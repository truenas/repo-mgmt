from mirror_mgmt.utils.paths import APTLY_CONF
from mirror_mgmt.utils.run import run


def aptly_run(command, **kwargs):
    return run(['aptly', '-config', APTLY_CONF] + command, **kwargs)
