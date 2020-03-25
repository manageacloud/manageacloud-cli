# To run the development version
#    make prepare
#    source ./venv/bin/activate
#    python  -m maccli.mac_cli

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

build-osx:prepare
	venv/bin/pip install --upgrade pip
	venv/bin/pip install pyinstaller
	venv/bin/pyinstaller mac.spec -y
	mv dist/mac mac
	mac/mac --version
	tar zcvf mac-Darwin-x86_64.tar.gz mac
	rm -rf mac
	mv mac-Darwin-x86_64.tar.gz dist/mac-Darwin-x86_64.tar.gz

publish-osx:build-osx
	scp dist/mac-Darwin-x86_64.tar.gz root@manageacloud.com:/var/www/downloads/
