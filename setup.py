from setuptools import setup

setup (name='mist.client',
       version='0.0.1',
       description='Python client for mist.io',
       url='https://github.com/mistio/mist.client',
       author= 'Chris Loukas',
       author_email='commixon@gmail.com',
       license='AGPLv3',
       packages=['mist'],
       install_requires=[
           'requests',
       ],
       zip_safe=False)
