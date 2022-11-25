#!/bin/bash

#
# NOTE: execute script from parent dir ..
#

function syntax()
{
	echo "ERROR  | missing/wrong param"
	echo "SYNTAX | $0 [ -p -c -a ]"
	echo "SYNTAX | -p push"
	echo "SYNTAX | -c autocommit"
	echo "SYNTAX | -a autocommit AND push"
}


PUSH=false
AUTOCOMMIT=false

if [ $# -gt 0 ]
then
	case "${1,,}" in
		"-p")
			PUSH=true
			echo PUSH=true
		;;
		"-c")
			AUTOCOMMIT=true
			echo AUTOCOMMIT=true
		;;
		"-a")
			AUTOCOMMIT=true
			echo AUTOCOMMIT=true
			PUSH=true
			echo PUSH=true
		;;
		"-h")
		;&
		*)
			syntax
			exit
		;;
	esac
else
	syntax
	exit
fi


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
