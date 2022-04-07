# To run the development version
#    make prepare
#    source ./venv/bin/activate
#    python  -m maccli.mac_cli

clean:
	rm -rf venv
	find . -name '*.pyc ' -delete

prepare:clean
	set -ex
	virtualenv venv -p /usr/bin/python3
	venv/bin/pip3 install -r requirements.txt
	#venv/bin/pip install .

test:prepare
	venv/bin/pip3 install mock nose
	venv/bin/python3 setup.py nosetests

publish-pypi:prepare
	# set up the api key at  $HOME/.pypirc (chmod 600)
	twine upload dist/*

build-osx:prepare
	venv/bin/pip3 install --upgrade pip
	venv/bin/pip3 install pyinstaller
	venv/bin/pyinstaller mac.spec -y
	mv dist/mac mac
	mac/mac --version
	tar zcvf mac-Darwin-x86_64.tar.gz mac
	rm -rf mac
	mv mac-Darwin-x86_64.tar.gz dist/mac-Darwin-x86_64.tar.gz

publish-osx:build-osx
	scp dist/mac-Darwin-x86_64.tar.gz root@manageacloud.com:/var/www/downloads/
