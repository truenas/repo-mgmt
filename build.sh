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
	gluster)
		scripts/update-ext-mirror gluster
		;;
	kubernetes)
		scripts/update-ext-mirror kubernetes
		;;
	helm)
		scripts/update-ext-mirror helm
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
