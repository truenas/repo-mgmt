#!/usr/bin/make -f
PYTHON?=/usr/bin/python3
COMMIT_HASH=$(shell git rev-parse --short HEAD)
REPO_CHANGED=$(shell if [ -d "./venv-$(COMMIT_HASH)" ]; then git status --porcelain | grep -c "mirror_mgmt/"; else echo "1"; fi)

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


update-mirrors: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt update_mirrors
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt create_mirrors_snapshots $(args)

update-repositories: check
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt update_repositories
	. ./venv-${COMMIT_HASH}/bin/activate && mirror_mgmt create_repositories_snapshots $(args)

update-debian:
	sh build.sh debmirror

update-debian-sid:
	sh build.sh debmirror-sid

update-truenas:
	sh build.sh truenasmirror

update-docker:
	sh build.sh docker

update-gluster:
	sh build.sh gluster

update-kubernetes:
	sh build.sh kubernetes

update-helm:
	sh build.sh helm

update-nvidia-docker:
	sh build.sh nvidia-docker

update-mirrorsss: update-debian update-docker update-gluster update-kubernetes update-nvidia-docker update-helm

push-repo:
	sh build.sh push-repo

# Sync and build all
all:
	echo "Available targets:"
	echo "update-debian     - Sync with upstream Debian repository"
	echo "update-docker     - Sync with upstream Docker repository"
	echo "update-gluster    - Sync with upstream Gluster repository"
	echo "update-kubernetes - Sync with upstream Kubernetes repository"
	echo "update-helm       - Sync with upstream helm repository"
	echo "update-nvidia-docker - Sync with upstream nvidia-docker repository"
	echo "update-truenas    - Update TrueNAS repo with local package directory"
	echo "push-repo         - Push merged repo to staging CDN"
	exit 1
