#!/usr/bin/make -f
PYTHON?=/usr/bin/python3
COMMIT_HASH=$(shell git rev-parse --short HEAD)
REPO_CHANGED=$(shell if [ -d "./venv-$(COMMIT_HASH)" ]; then git status --porcelain | grep -c "mirror_mgmt/"; else echo "1"; fi)
SNAPSHOT_SUFFIX := $(or ${SNAPSHOT_SUFFIX}, devel)

.DEFAULT_GOAL := all

check:
ifneq ($(REPO_CHANGED),0)
	@echo "Setting up new virtual environment"
	@rm -rf venv-*
	@${PYTHON} -m pip install -U virtualenv >/dev/null 2>&1 || { echo "Failed to install/upgrade virtualenv package"; exit 1; }
	@${PYTHON} -m venv venv-${COMMIT_HASH} || { echo "Failed to create virutal environment"; exit 1; }
	@{ . ./venv-${COMMIT_HASH}/bin/activate && \
		python3 -m pip install -r requirements.txt >/dev/null 2>&1 && \
		python3 setup.py install >/dev/null 2>&1; } || { echo "Failed to install mirror-mgmt"; exit 1; }
endif


clean-mirrors: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt clean_mirrors

clean: check clean-mirrors

clean-dangling-snapshots: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt clean_dangling

backup: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt backup

update-mirrors-without-backup: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt update_mirrors
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt create_mirrors_snapshots -ps --snapshot-suffix=${SNAPSHOT_SUFFIX}

validate_manifest: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt validate --no-validate-system_state

update-mirrors: backup update-mirrors-without-backup

publish: backup
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt create_mirrors_snapshots -ps --snapshot-suffix=${SNAPSHOT_SUFFIX}

# Sync and build all
all: backup update-mirrors-without-backup
