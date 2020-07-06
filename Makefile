lint:
	flake8 .

freeze:
	pip freeze > requirements.txt

init:
	pip install -r requirements.txt
