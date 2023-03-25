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
$NO_OPTIONS && { 
	info "no options detected, PULL ENABLED"
	PULL=true
}
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
for directory in ${PROJECT_DIRS[@]}
do
	# check for dir existence
	if [ ! -d "${directory}" ]
	then
		fatal "${directory} | does not exist"
		exit 1
	fi
	# check for git repo
	if [ ! -d "${directory}/.git/" ]
	then
		warn "${directory} | not a git repo"
		continue
	fi
	# PULL
	if $PULL
	then
		info "PULL       | ${directory}"
		(cd "${directory}"; git pull)
	fi
	# AUTOCOMMIT
	if $AUTOCOMMIT
	then
		info "AUTOCOMMIT | ${directory}"
		(
			cd $d
			git add .
			git commit -am "autoupdate"
		)
	fi
	# PUSH
	if $PUSH 
	then
		info "PUSH       | ${directory}"
		(cd "${directory}"; git push)
	fi
done
