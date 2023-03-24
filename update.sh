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
. "${HERE}/dump_vars.include"
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
DEFAULT_DIRFILE="${HERE}/dirs.txt"
DIRFILE=
AUTODISCOVER_CONFIG="${HERE}/autodiscover.config"
AUTODISCOVER=true

parse_options "${@}"
#
# default
#
$NO_OPTIONS && { echo 'INFO   | no options detected, PULL ENABLED';PULL=true; }
#
# always use last version
#
$GIT_AUTOUPDATE && git_autoupdate
#
# list working dihprints this help and exits
# list working PROJECT_DIRS
#
if [ ${DIRFILE:-UNDEFINED} == UNDEFINED ]
then
	DIRFILE="${DEFAULT_DIRFILE}"
else
	AUTODISCOVER=false
fi
${JUST_LISTDIRS} && AUTODISCOVER=false
${AUTODISCOVER} && autodiscover || list_dirs

dump_vars
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
