#!/bin/bash

#
# NOTE: execute script from parent dir ..
#
HERE="$(dirname ${BASH_SOURCE[0]})"
. "${HERE}/syntax.include"
. "${HERE}/git_autoupdate.include"
. "${HERE}/list_dirs.include"
. "${HERE}/autodiscover.include"
# 
# set defaults
#
PULL=true
PUSH=false
AUTOCOMMIT=false
PROJECT_DIRS=()
JUST_LISTDIRS=false
NO_OPTIONS=false
GIT_AUTOUPDATE=true
DIRFILE="${HERE}/PROJECT_DIRS.txt"
AUTODISCOVER_CONFIG="${HERE}/autodiscover.config"
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
# list working PROJECT_DIRS
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
for d in ${PROJECT_DIRS[@]}
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
