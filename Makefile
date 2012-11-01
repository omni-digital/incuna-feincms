SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make release -- add to internal pypi"

release:
	python setup.py register -r incuna sdist upload -r incuna
