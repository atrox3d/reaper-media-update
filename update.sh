#!/bin/bash

#
# NOTE: execute script from parent dir ..
#

#
# prints script syntax
#
function syntax()
{
	echo "SYNTAX | $0 [ -lpcxun ]"
	echo "SYNTAX | -l list dirs and exits"
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -x autocommit AND push"
	echo "SYNTAX | -u pull (default)"
	echo "SYNTAX | -n no autoupdate script"
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
# 
# parse options
# 
OPTIND=1
while getopts ":lpcxhun" option
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
# list working dirs
#
list_dirs
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
