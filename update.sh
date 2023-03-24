#!/bin/bash

#
# NOTE: execute script from parent dir ..
#

#
# prints script syntax
#
function syntax()
{
	echo "SYNTAX | $0 [ -hlpcxun -f {dir-file} ]"
	echo "SYNTAX | -h prints this help and exits"
	echo "SYNTAX | -l list dirs and exits"
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -x autocommit AND push"
	echo "SYNTAX | -u pull (default)"
	echo "SYNTAX | -n no autoupdate script"
	echo "SYNTAX | -f {dir-file} | use {dir-file as input}"
}
#
# updates this script
#
function git_autoupdate()
{
	local here="$(dirname ${BASH_SOURCE[0]})"
	(
		echo "INFO   | GIT AUTOUPDATE SCRIPT | cd ${here}..."
		cd "${here}"
		echo "INFO   | GIT AUTOUPDATE SCRIPT | git pull..."
		git pull
	)
}
#
# read input dirs from file into array
#
function list_dirs()
{
	echo "INFO   | reading from ${DIRFILE}..."
	dirs=($(cat "${DIRFILE}" | sort))
	echo "INFO   | found ${#dirs[@]} dirs:"

	for d in "${dirs[@]}"
	do
		echo "INFO   | ${d}"
	done
	
	if $JUST_LISTDIRS
	then
		exit
	fi
}
#
# autodiscover
#
function autodiscover()
{
	# check if autodiscover config exists
	[ -f ${AUTODISCOVER_CONFIG} ] || {
		echo "FATAL   | ${AUTODISCOVER_CONFIG} does not exist"
		exit 1
	}
	# get list of roots in array
	roots=($(cat "${AUTODISCOVER_CONFIG}" | sort))
	echo "INFO   | found ${#roots[@]} roots:"

	for root in "${roots[@]}"
	do
		echo "INFO   | ${root}"
	done
	exit
}
# 
# set defaults
#
PULL=true
PUSH=false
AUTOCOMMIT=false
JUST_LISTDIRS=false
NO_OPTIONS=false
GIT_AUTOUPDATE=true
HERE="$(dirname ${BASH_SOURCE[0]})"
DIRFILE="${HERE}/dirs.txt"
AUTODISCOVER_CONFIG="${HERE}/.autodiscover.config"
# 
# parse options
# 
OPTIND=1
while getopts ":lpcxhunf:" option
do
	case $option in
		u)
			PULL=true
			echo "INFO   | PULL enabled"
		;;
		l)
			JUST_LISTDIRS=true
			echo "INFO   | JUST_LISTDIRS enabled"
		;;
		p)
			PUSH=true
			echo "INFO   | PUSH enabled"
		;;
		c)
			AUTOCOMMIT=true
			echo "INFO   | AUTOCOMMIT enabled"
		;;
		x)
			AUTOCOMMIT=true
			echo "INFO   | AUTOCOMMIT enabled"
			PUSH=true
			echo "INFO   | PUSH enabled"
		;;
		n)
			echo "INFO   | GIT AUTOUPDATE disabled"
			GIT_AUTOUPDATE=false
		;;
		f)
			DIRFILE="${HERE}/${OPTARG}"
			echo "INFO   | DIRFILE=${DIRFILE}"
			[ -f "${DIRFILE}" ] || {
				echo "FATAL  | ${DIRFILE} does not exists"
				ls -l
				exit 1
			}
		;;
		#
		# start fallthrough for invalid/missing options and help
		#
		\?)
			echo "ERROR  | invalid option -$OPTARG"
		;;&
		:)
			echo "ERROR  | missing option arg, flag -$OPTARG"
		;;&
		h)
			echo "INFO   | HELP"
		;;&
		*)
			syntax
			exit
		;;
	esac
done
#
# no options passed
#
if [ $OPTIND -eq 1 ]
then
	NO_OPTIONS=true
fi 
shift "$((OPTIND-1))"
#
# always use last version
#
if $GIT_AUTOUPDATE
then
	git_autoupdate
fi
#
# list working dihprints this help and exits
# list working dirs
#
# list_dirs
autodiscover
#
# default
#
if $NO_OPTIONS
then
	echo 'INFO   | no options detected, PULL ENABLED'
	PULL=true
fi
#
# MAIN LOOP
#
for d in ${dirs[@]}
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
