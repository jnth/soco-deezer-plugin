clean:
	rm -rf build dist *.egg-info

build:
	python3.7 setup.py bdist_wheel
	python3.7 setup.py sdist

test:
	python3.7 -m unittest discover tests