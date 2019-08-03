#!/usr/bin/make -f

update-debian:
	sh build.sh debmirror

update-truenas:
	sh build.sh truenasmirror

update-mirrors: update-debian update-truenas

merge-repos:
	sh build.sh merge-repos

push-repo:
	sh build.sh push-repo

# Sync and build all
all:
	echo "Available targets:"
	echo "update-debian - Sync with upstream Debian repository"
	echo "update-truenas - Sync with local buildd TrueNAS repository"
	echo "merge-repos - Merge and sign the debian + truenas repo"
	echo "push-repo - Push merged repo to staging CDN"
	exit 1
