from setuptools import setup

setup (name='mist.client',
       version='0.0.1',
       description='Python client for mist.io',
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
       packages=['mist'],
       install_requires=[
           'requests',
       ],
       zip_safe=False)
