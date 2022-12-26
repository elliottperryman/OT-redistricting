#! /bin/sh
# Creates and sources the virtual environment then install the required packages
# If the directory already exists, just sources the venv
if [ -d ./Sem ]; then 
	source ./Sem/bin/activate
else
	python -m venv Sem
	source ./Sem/bin/activate
	python -m pip -r requirements.txt
fi

