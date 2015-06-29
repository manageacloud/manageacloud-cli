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
    version=find_version('maccli', '__init__.py'),
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts':
            ['mac = maccli.mac_cli:main']
    },
    include_package_data=True,
    author='R3Systems Pty Ltd',
    author_email='support@manageacloud.com',
    description='Automation Swiss Army knife',
    license='Apache v2',
    keywords='manageacloud docker puppet chef saltstack ansible bash rackspace aws digitalocean '
             'gce google compute engine multicloud multi-cloud orchestration ci cd continuous integration deployment a/b testing',
    url='https://manageacloud.com',
    test_suite='tests',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Programming Language :: Python'

    ]

)
