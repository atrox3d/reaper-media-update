#!/bin/bash

#
# NOTE: execute script from parent dir ..
#
echo "${0}"
HERE="$(dirname ${0})"
# echo "${HERE}"
# cd "$HERE"
# ls
# exit
cd "${HERE}/.."
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
READ_DIRS=false

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
	READ_DIRS=true
	AUTODISCOVER=false
fi
#
# print all vars
#
dump_vars
#
# populate array of directories
#
${AUTODISCOVER} && autodiscover
${READ_DIRS} && read_dirs

${JUST_LISTDIRS} && list_dirs
#
# MAIN LOOP
#
for directory in ${PROJECT_DIRS[@]}
do
	echo '######################################################################'
	echo '#                                                                    #'
	echo '#                  '"${directory^^}"
	echo '#                                                                    #'
	echo '######################################################################'
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
		[ $? == 0 ] || {
			fatal "errorlevel is not zero"
			exit $?
		}
	fi
	# AUTOCOMMIT
	if $AUTOCOMMIT
	then
		info "AUTOCOMMIT | ${directory}"
		(
			cd "${directory}"
			git add .
			git commit -am "autoupdate"
		)
		[ $? == 0 ] || {
			fatal "errorlevel is not zero"
			exit $?
		}
	fi
	# PUSH
	if $PUSH 
	then
		info "PUSH       | ${directory}"
		(cd "${directory}"; git push)
		[ $? == 0 ] || {
			fatal "errorlevel is not zero"
			exit $?
		}
	fi
done
