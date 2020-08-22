# Definition of automated processes and recuring task in the WDC project

#
# Determine if all python code conforms with the PEP8 guidelines
# Exceptions and configuration provided in the .flake8 file
lint:
	flake8 .

#
# Use autopep8 to correct common formatting mistakes in all python files in the:
# - wdc folder
# - tests folder
# - setup.py in the root folder
pep8:
	find wdc/ -name '*.py' -exec autopep8 --in-place '{}' \;
	find tests/ -name '*.py' -exec autopep8 --in-place '{}' \;
	autopep8 --in-place setup.py

#
# Writtes all installed pip packages into the requirements.txt
freeze:
	pip freeze > requirements.txt

#
# Install all packages defined in the requirements.txt
init:
	pip install -r requirements.txt

#
# Runs unit tests defined in the wdc project
test:
	python -m unittest discover tests "*_tests.py"

#
# Install the wdc from code
install:
	python setup.py install

#
# runs a series of taks that should be done before pushing to the repository
ci: pep8 lint test

#
# Creates distribution packages for the wdc
dist: clean
	python setup.py sdist --formats=gztar,zip
	python setup.py bdist_wheel

#
# Create only the wheel file fo pypi upload purposes
whl: clean
	python setup.py bdist_wheel

#
# Removed all generated directories
clean:
	rm -rf dist
	rm -rf build
	rm -rf wdc.egg-info

#
# Creates a local docker image from the current state of the application
docker: dist
	sudo docker build . -t wdc:dev-latest --build-arg VERSION=latest

#
# Starts a docker image with the latest build version of wdc and drops you into the cli in that docker image
playground: docker
	sudo docker run -it -v $(shell pwd):/wdccode wdc:dev-latest sh
