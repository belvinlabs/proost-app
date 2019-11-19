#!/bin/bash

# Display colorized warning output
function cwarn() {
	COLOR='\033[01;31m'	# bold red
	RESET='\033[00;00m'	# normal white
	MESSAGE=${@:-"${RESET}Error: No message passed"}
	echo -e "${COLOR}${MESSAGE}${RESET}"
}

cwarn "The migrate functionality picks up most of the changes made "\
"to models, but not all changes to models are detected. Please "\
"review your changes int hte migrations folder and if no new "\
"revision is made, you can use revision.sh to generate one manually."\
"\nMore inforation on what changes can be detected: "\
"https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does"\
"-autogenerate-detect-and-what-does-it-not-detect"



export FLASK_APP=src/main
flask db migrate