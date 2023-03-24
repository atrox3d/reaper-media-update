#!/bin/bash

#
# NOTE: execute script from parent dir ..
#
HERE="$(dirname ${BASH_SOURCE[0]})"
. "${HERE}/syntax.include"
. "${HERE}/git_autoupdate.include"
. "${HERE}/list_dirs.include"
. "${HERE}/autodiscover.include"
. "${HERE}/parse-options.include"
# 
# set defaults
#
PULL=true
PUSH=false
AUTOCOMMIT=false
PROJECT_DIRS=()
JUST_LISTDIRS=false
NO_OPTIONS=false
GIT_AUTOUPDATE=true
DIRFILE="${HERE}/dirs.txt"
AUTODISCOVER_CONFIG="${HERE}/autodiscover.config"
AUTODISCOVER=true

parse_options "${@}"
#
# default
#
$NO_OPTIONS && { echo 'INFO   | no options detected, PULL ENABLED';PULL=true; }
VARS=(
PULL
PUSH
AUTOCOMMIT
PROJECT_DIRS
JUST_LISTDIRS
NO_OPTIONS
GIT_AUTOUPDATE
DIRFILE
AUTODISCOVER_CONFIG
AUTODISCOVER
)
#
# always use last version
#
$GIT_AUTOUPDATE && git_autoupdate
#
# list working dihprints this help and exits
# list working PROJECT_DIRS
#
$JUST_LISTDIRS && AUTODISCOVER=false
$AUTODISCOVER && autodiscover || list_dirs
for v in "${VARS[@]}"
do
	echo "INFO  | var | $v=${!v}"
done
exit
#
# MAIN LOOP
#
for d in ${PROJECT_DIRS[@]}
do
	#
	# PULL
	#
	if $PULL
	then
		echo "INFO   | "${d^^}" | PULL..."
		(cd $d; git pull)
	fi
	#
	# AUTOCOMMIT
	#
	if $AUTOCOMMIT
	then
		echo "INFO   | "${d^^}" | AUTOCOMMIT..."
		(
			cd $d
			git add .
			git commit -am "autoupdate"
		)
	fi
	#
	# PUSH
	#
	if $PUSH 
	then
		echo "INFO   | "${d^^}" | PUSH..."
		(cd $d; git push)
	fi
done
