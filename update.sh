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
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -a autocommit AND push"
}
# 
# set defaults
# 
PUSH=false
AUTOCOMMIT=false
# 
# parse options
# 
OPTIND=1
while getopts ":pcah" option
do
	case $option in
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
if [ $OPTIND -eq 1 ]
then
	syntax
	exit
fi 
shift "$((OPTIND-1))"
#
# read input dirs from file into array
#
HERE="$(dirname ${BASH_SOURCE[0]})"
DIRFILE="${HERE}/dirs.txt"
echo "INFO   | reading from ${DIRFILE}..."
dirs=($(cat "${DIRFILE}"))
echo "INFO   | found ${#dirs[@]} dirs:"
for d in "${dirs[@]}"
do
	echo "INFO   | ${d}"
done
#
# MAIN LOOP
#
for d in ${dirs[@]}
do
	#
	# PULL
	#
	echo "INFO   | "${d^^}" | pulling $d..."
	(cd $d; git pull)
	#
	# AUTOCOMMIT
	#
	if $AUTOCOMMIT
	then
		echo "INFO   | "${d^^}" | AUTOCOMMIT ENABLED | auto committing ..."
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
		echo "INFO   | "${d^^}" | PUSH ENABLED | pushing ..."
		(cd $d; git push)
	fi
done
