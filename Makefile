#!/usr/bin/make -f

update-debian:
	sh build.sh debmirror

update-truenas:
	sh build.sh truenasmirror

update-docker:
	sh build.sh docker

update-gluster:
	sh build.sh gluster

update-mirrors: update-debian update-docker update-gluster update-truenas

merge-repos:
	sh build.sh merge

push-repo:
	sh build.sh push-repo

zfs:
	sh build.sh zfs

# Sync and build all
all:
	echo "Available targets:"
	echo "update-debian - Sync with upstream Debian repository"
	echo "update-truenas - Sync with local buildd TrueNAS repository"
	echo "merge-repos - Merge and sign the debian + truenas repo"
	echo "push-repo - Push merged repo to staging CDN"
	echo "zfs - Build zfs-modules package from zfs-dkms"
	exit 1
