#!/usr/bin/make -f

update-debian:
	sh build.sh debmirror

update-truenas:
	sh build.sh truenasmirror

update-docker:
	sh build.sh docker

update-gluster:
	sh build.sh gluster

update-kubernetes:
	sh build.sh kubernetes

update-mirrors: update-debian update-docker update-gluster update-kubernetes

push-repo:
	sh build.sh push-repo

# Sync and build all
all:
	echo "Available targets:"
	echo "update-debian  - Sync with upstream Debian repository"
	echo "update-docker  - Sync with upstream Docker repository"
	echo "update-gluster - Sync with upstream Gluster repository"
	echo "update-kubernetes - Sync with upstream Kubernetes repository"
	echo "update-truenas - Update TrueNAS repo with local package directory"
	echo "push-repo      - Push merged repo to staging CDN"
	exit 1
