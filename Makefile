clean:
	rm -rf venv
	find . -name '*.pyc ' -delete

prepare:clean
	set -ex
	virtualenv venv -p /usr/bin/python2.7
	venv/bin/pip install -r requirements.txt
	#venv/bin/pip install .

test:prepare
	venv/bin/pip install mock nose
	venv/bin/python setup.py nosetests

publish-pypi:prepare
	python setup.py sdist upload