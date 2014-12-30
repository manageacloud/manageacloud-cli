import re
import os
import codecs

from setuptools import setup, find_packages


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='mac',
    version=find_version('mac', '__init__.py'),
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['mac = cli.mac_cli:main']
    },
    include_package_data=True,
    author='R3Systems Pty Ltd',
    author_email='support@manageacloud.com',
    description='CLI for Manageacloud',
    license='Apache v2',
    keywords='manageacloud docker puppet chef rackspace aws digitalocean',
    url='https://manageacloud.com',
    test_suite='tests',
)
