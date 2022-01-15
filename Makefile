.ONESHELL:
.PHONY: check clean build virtual test install publish bdist_wheel bdist sdist

# If `venv/bin/python` exists, it is used. If not, use PATH to find python.
PWD=$(shell pwd)
VENV           = $(PWD)/venv
SYSTEM_PYTHON  = $(or $(shell which python3), $(shell which python))
PYTHON         = $(VENV)/bin/python

WHEEL=$(shell find dist -name '*.whl')

build: clean check test bdist_wheel

check: virtual
	@echo "Verifying package metadata"
	$(PYTHON) setup.py check -sm

virtual:
	$(SYSTEM_PYTHON) -m venv --system-site-packages $(VENV) 
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r build_requirements.txt -r test_requirements.txt

test: virtual
	#cd src/main && $(PYTHON) -m pytest ../test/ --verbosity=1
	cd src/main && $(PYTHON) -m pytest --verbosity=5 ../test/ 

install: virtual build
	pip install $(WHEEL)

publish: build
	twine upload --repository pypi $(WHEEL)

clean:
	$(SYSTEM_PYTHON) setup.py clean --all
	rm -fr dist/ build/ .out .pytest_cache *.egg-info $(VENV)

bdist_wheel: virtual 
	$(PYTHON) setup.py bdist_wheel

sdist: virtual
	$(PYTHON) setup.py sdist

bdist: virtual
	$(PYTHON) setup.py bdist \
  --formats=rpm \
  --formats=gztar \
  --formats=bztar \
  --formats=xztar \
  --formats=ztar \
  --formats=tar \
  --formats=zip \
  --formats=msi \
  --formats=egg

