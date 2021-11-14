import os

from mirror_mgmt.config import MGMT_DIR


CONF_DIR = os.path.join(MGMT_DIR, 'conf')
APTLY_CONF = os.path.join(CONF_DIR, 'aptly.conf')
MANIFEST_PATH = os.path.join(CONF_DIR, 'manifest.yaml')
