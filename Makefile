clean:
	rm -rf build dist *.egg-info

build:
	python3.6 setup.py bdist_wheel
	python3.6 setup.py sdist
