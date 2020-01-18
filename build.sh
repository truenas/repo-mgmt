#!/bin/sh

. ./conf/config.env

exit_err() {
	echo "$@"
	exit 1
}

case $1 in
	truenasmirror)
		scripts/update-mirror truenas
		;;
	debmirror)
		scripts/update-mirror debian
		;;
	docker)
		scripts/update-ext-mirror docker
		;;
	merge)
		scripts/update-mirror merge
		;;
	zfs)
		scripts/build-zfs-chroot
		;;
	*)
		exit_err "Invalid option selected"
		;;
esac
