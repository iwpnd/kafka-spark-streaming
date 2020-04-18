.PHONY: all install test

VENV_NAME=venv
VENV_BIN=${VENV_NAME}/bin
PYTHON=${VENV_BIN}/python

all:
	@echo "make prepare-dev"
	@echo "    Create python virtual environment and install dependencies."
	@echo "make test"
	@echo "    Run tests on project."

install:
	which virtualenv || python -m pip install virtualenv
	virtualenv $(VENV_NAME)
	${PYTHON} -m pip install -U pip setuptools
	${PYTHON} -m pip install -r producer/requirements.txt
	make test

test:
	${PYTHON} -m pytest --cov=producer --cov=consumer --cov=monitor -v
