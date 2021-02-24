#!/bin/bash

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

NUM_ARGS_REQUIRED=0
if [ $# -ne "${NUM_ARGS_REQUIRED}" ]; then
	cat <<EOF
Usage: $0
EOF
	exit 1
fi

run() {
	echo "+" "$@" 1>&2
	"$@"
}

color() {
	COLOR=$1
	MESSAGE=$2
	case "${COLOR}" in
	red)
		echo -e "\e[31m${MESSAGE}\e[39m"
		;;
	blue)
		echo -e "\e[94m${MESSAGE}\e[39m"
		;;
	green)
		echo -e "\e[32m${MESSAGE}\e[39m"
		;;
	*)
		echo "Unrecognized color: ${COLOR}" 1>&2
		echo -e "${MESSAGE}"
		;;
	esac
}

mkdir -p zipcodes_by_states
mkdir -p zipcodes_to_latlong_by_state

run python zipcode_extractor.py

for state in zipcodes_by_states/*; do
	run python create_zipcode_to_latlon.py "${state}" "zipcodes_to_latlong_by_state/$(basename "${state%.json}")" >|"${state%.log}"
done
