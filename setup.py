import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests',
    'argparse',
    'argcomplete',
    'pyyaml',
    'prettytable',
    'ansible'
]


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='mist',
    version='1.0.0',
    description='Python client for mist.io',
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    url='https://github.com/mistio/mist.client',
    keywords='web cloud server management monitoring automation mobile libcloud pyramid amazon aws rackspace openstack linode softlayer digitalocean gce',
    author='Chris Loukas',
    author_email='commixon@gmail.com',
    license='GPLv3',
    packages=find_packages('src'),
    scripts=['src/mistcommand/mist',
             'src/mistansible/mistplay'],
    package_dir={'': 'src'},
    install_requires=requires,
    zip_safe=False,
    include_package_data=True
)
