#!/bin/bash

#
# NOTE: execute script from parent dir ..
#
HERE="$(dirname ${BASH_SOURCE[0]})"
. "${HERE}/loader.include"

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
# default: no options
#
$NO_OPTIONS && { echo 'INFO   | no options detected, PULL ENABLED';PULL=true; }
#
# always use last version
#
$GIT_AUTOUPDATE && git_autoupdate
#
# set variables
#
if [ ${DIRFILE:-UNDEFINED} == UNDEFINED ]
then
	DIRFILE="${DEFAULT_DIRFILE}"
else
	AUTODISCOVER=false
fi
${JUST_LISTDIRS} && AUTODISCOVER=false
#
# populate array of directories
#
${AUTODISCOVER} && autodiscover || list_dirs
#
# print all vars
#
dump_vars
#
# MAIN LOOP
#
for d in ${PROJECT_DIRS[@]}
do
	#
	# check for dir existence
	#
	if [ ! -d "${d}" ]
	then
		echo "FATAL | ${d} | does not exist"
		exit 1
	fi
	#
	# check for git repo
	#
	if [ ! -d "${d}/.git/" ]
	then
		echo "WARNING | ${d} | not a git repo"
		continue
	fi
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
