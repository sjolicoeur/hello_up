.PHONY: docs test

help:
	@echo "  createvenv  create a virtualenv using python3"
	@echo "  env         create a development environment using virtualenv"
	@echo "  deps        install dependencies using pip"
	@echo "  clean       remove unwanted files like .pyc's"
	@echo "  lint        check style with flake8"
	@echo "  test        run all your tests using py.test"

createvenv:
	python3  -m venv venv
env:
	sudo easy_install pip && \
	pip install virtualenv && \
	virtualenv env && \
	. env/bin/activate && \
	make deps

deps:
	pip install -r requirements.txt

clean:
	python manage.py clean

lint:
	flake8 --exclude=venv .

test:
	py.test tests
