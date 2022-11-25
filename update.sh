#!/bin/bash

#
# NOTE: execute script from parent dir ..
#

function syntax()
{
	# echo "ERROR  | missing/wrong param"
	echo "SYNTAX | $0 [ -p -c -a ]"
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -a autocommit AND push"
}


PUSH=false
AUTOCOMMIT=false

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
		\?)
			echo "ERROR  | invalid option -$OPTARG"
		;;&
		:)
			echo "ERROR  | missing option arg, flag -$OPTARG"
		;;&
		h)
			echo HELP
		;;&
		*)
			# echo 'star *, ' "option -$option OPTARG $OPTARG"
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


dirs=(
	black-hole-sun black-hole-sun-moises
	man-in-the-box man-in-the-box-moises
	cochise cochise-moises 
	spoonman spoonman-moises 
	killing-in-the-name-of-moises
)

for d in ${dirs[@]}
do
	echo "INFO | pulling $d..."
	(cd $d; git pull)

	if $AUTOCOMMIT
	then
		echo "INFO | auto committing $d..."
		(
			cd $d
			git add .
			git commit -am "autoupdate"
		)
	fi

	if $PUSH 
	then
		echo "INFO | pushing $d..."
		(cd $d; git push)
	fi
done
