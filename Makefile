

PYTHON=python3
WHEEL=$(shell find dist -name '*.whl')

build: clean test bdist_wheel

test:
	cd src/main && python -m pytest ../test/ --verbosity=1

publish: build
	twine upload --repository pypi $(WHEEL)

install: build
	pip install $(WHEEL)

clean:
	rm -fr dist/ build/

bdist_wheel:
	$(PYTHON) setup.py bdist_wheel

sdist:
	$(PYTHON) setup.py sdist

bdist:
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

