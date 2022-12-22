#! /bin/sh
# Creates and sources the virtual environment then install the required packages
if [ -d ./Sem]; then 
	source ./Sem/bin/activate;
else
	python -m venv Sem
	source ./Sem/bin/activate;
fi

python -m pip -r requirements.txt
