from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup (name='mistpy',
       version='0.0.1',
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
       author='Chris Loukas',
       author_email='commixon@gmail.com',
       license='AGPLv3',
       packages=['mistpy'],
       install_requires=[
           'requests',
       ],
       zip_safe=False)
