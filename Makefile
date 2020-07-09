lint:
	flake8 .

freeze:
	pip freeze > requirements.txt

init:
	pip install -r requirements.txt

test:
	python -m unittest discover tests "*_tests.py"

install:
	python setup.py install
