#!/bin/bash

#
# NOTE: execute script from parent dir ..
#

#
# prints script syntax
#
function syntax()
{
	echo "SYNTAX | $0 [ -p -c -a ]"
	echo "SYNTAX | -l list dirs and exits"
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -a autocommit AND push"
	echo "SYNTAX | -u pull (default)"
}
# 
# set defaults
#
PULL=false
PUSH=false
AUTOCOMMIT=false
LISTDIRS=false
NO_OPTIONS=false
HERE="$(dirname ${BASH_SOURCE[0]})"
DIRFILE="${HERE}/dirs.txt"
# 
# parse options
# 
OPTIND=1
while getopts ":lpcahu" option
do
	case $option in
		u)
			PULL=true
		;;
		l)
			LISTDIRS=true
		;;
		p)
			PUSH=true
			echo "INFO   | PUSH enabled"
		;;
		c)
			AUTOCOMMIT=true
			echo "INFO   | AUTOCOMMIT enabled"
		;;
		a)
			AUTOCOMMIT=true
			echo "INFO   | AUTOCOMMIT enabled"
			PUSH=true
			echo "INFO   | PUSH enabled"
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
# read input dirs from file into array
#
echo "INFO   | reading from ${DIRFILE}..."
dirs=($(cat "${DIRFILE}"))
echo "INFO   | found ${#dirs[@]} dirs:"
for d in "${dirs[@]}"
do
	echo "INFO   | ${d}"
done
if $LISTDIRS
then
	exit
fi
#
# MAIN LOOP
#
if $NO_OPTIONS
then
	echo 'INFO   | no options detected, PULL ENABLED'
	PULL=true
fi
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
