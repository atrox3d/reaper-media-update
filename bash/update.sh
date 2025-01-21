#!/usr/bin/env bash

#
# NOTE: execute script from parent dir ..
#
echo "${0}"
HERE="$(dirname ${0})"
echo "HERE=${HERE}"
#exit
# cd "$HERE"
# ls
# exit
#cd "${HERE}/.."
. "${HERE}/loader.include"

logger_setlevel INFO

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
IGNORE_ERRORS=false
MATCH=""

parse_options "${@}"
#######################################################
# default: no options
#######################################################
$NO_OPTIONS && { 
	info "no options detected, PULL ENABLED"
	PULL=true
}
#######################################################
# always use last version
#######################################################
$GIT_AUTOUPDATE && git_autoupdate
#######################################################
# set variables
#######################################################
if [ ${DIRFILE:-UNDEFINED} == UNDEFINED ]
then
	DIRFILE="${DEFAULT_DIRFILE}"
else
	READ_DIRS=true
	AUTODISCOVER=false
fi
#######################################################
# print all vars
#######################################################
dump_vars
#######################################################
# populate array of directories PROJECT_DIRS
#######################################################
${AUTODISCOVER} && autodiscover
${READ_DIRS} && read_dirs

${JUST_LISTDIRS} && list_dirs

function die()
{
	local exitcode=$?
	fatal "${@}"
	dump_vars
	exit $exitcode
}

if [ "${MATCH:-EMPTY}" != "EMPTY" ]
then
	info "matching dirs with '*${MATCH}*'..."
	DIRS=()
	for directory in "${PROJECT_DIRS[@]}"
	do
		debug "matching dir: '${directory}' with '*${MATCH}*'..."
		case "${directory}" in
			*"${MATCH}"*)
				debug "MATCH! dir '${directory}'"
				DIRS+=("${directory}")
			;;
			*)
				debug "NO MATCH! dir '${directory}'"
			;;
		esac
	done
else
	DIRS=("${PROJECT_DIRS[@]}")
fi
#######################################################
# MAIN LOOP
#######################################################
for directory in "${DIRS[@]}"
do
	echo '######################################################################'
	echo '#                                                                    #'
	echo '#                  '"${directory^^}"
	echo '#                                                                    #'
	echo '######################################################################'
	#######################################################
	# check for dir existence
	#######################################################
	if [ ! -d "${directory}" ]
	then
		fatal "${directory} | does not exist"
		exit 1
	fi
	#######################################################
	# check for git repo
	#######################################################
	if [ ! -d "${directory}/.git/" ]
	then
		warn "${directory} | not a git repo, SKIPPING"
		continue
	fi
	#######################################################
	# check for remotes
	#######################################################
	remote="$(cd "${directory}"; git remote -v)"
	if [ "${remote:-NOREMOTE}" == NOREMOTE ]
	then
		warn "${directory} | has no remotes, SKIPPING"
		continue
	fi
	#######################################################
	# PULL
	#######################################################
	if $PULL
	then
		DONE_PULL=false
		while ! $DONE_PULL
		do
			info "SWITCH     | macOS"
			(
				cd "${directory}"
				git switch macOS
			)
			info "PULL       | ${directory}"
			PULL_OUTPUT="$(
							cd "${directory}"
							git pull 2>&1
						)"
			exitcode=$?
			echo "$PULL_OUTPUT"
			echo "exitcode: $exitcode"
			if [ $exitcode -ne 0 ]
			then
				grep -iq "error in the HTTP2 framing layer" <<< "$PULL_OUTPUT" && {
					echo "retrying..."
					sleep 2
					continue
				}
				$IGNORE_ERRORS && {
					warn "exit code was $exitcode"
				} || {
					die "errorlevel is not zero: $exitcode"
				}
			else
				DONE_PULL=true
			fi
		done
	fi
	#######################################################
	# AUTOCOMMIT
	#######################################################
	if $AUTOCOMMIT
	then
		info "AUTOCOMMIT | ${directory}"
		(
			cd "${directory}"
			git add .
			git commit -am "autoupdate"
		)
		exitcode=$?
		if [ $exitcode -ne 0 ]
		then
			$IGNORE_ERRORS && {
				warn "exit code was $exitcode"
			} || {
				die "errorlevel is not zero: $exitcode"
			}
		fi
	fi
	#######################################################
	# PUSH
	#######################################################
	if $PUSH 
	then
		info "PUSH       | ${directory}"
		(cd "${directory}"; git push)
		exitcode=$?
		if [ $exitcode -ne 0 ]
		then
			$IGNORE_ERRORS && {
				warn "exit code was $exitcode"
			} || {
				die "errorlevel is not zero: $exitcode"
			}
		fi
	fi
done
