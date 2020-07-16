lint:
	flake8 .

pep8:
	find wdc/ -name '*.py' -exec autopep8 --in-place '{}' \;
	find tests/ -name '*.py' -exec autopep8 --in-place '{}' \;
	autopep8 --in-place setup.py

freeze:
	pip freeze > requirements.txt

init:
	pip install -r requirements.txt

test:
	python -m unittest discover tests "*_tests.py"

install:
	python setup.py install

ci: pep8 lint test

