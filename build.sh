#!/bin/sh

. ./conf/config.env

exit_err() {
	echo "$@"
	exit 1
}

case $1 in
	truenasmirror)
		scripts/update-truenas
		;;
	debmirror)
		scripts/update-debian
		;;
	docker)
		scripts/update-ext-mirror docker
		;;
	ceph)
		scripts/update-ext-mirror ceph
		;;
	gluster)
		scripts/update-ext-mirror gluster
		;;
	kubernetes)
		scripts/update-ext-mirror kubernetes
		;;
	nvidia-docker)
		scripts/update-ext-mirror libnvidia
		scripts/update-ext-mirror nvidia-container
		scripts/update-ext-mirror nvidia-docker
		;;
	*)
		exit_err "Invalid option selected"
		;;
esac
