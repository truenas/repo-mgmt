#!/bin/sh

. ./conf/confg.env

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
	merge-repos)
		;;
	*)
		exit_err "Invalid option selected"
		;;
esac
