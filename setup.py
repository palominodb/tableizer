
from setuptools import setup, find_packages

setup(
    name='tableizer',
    version='0.1.0',
    author='Moss Gross',
    author_email='moss@palominodb.com',
    packages=['tableizer', 'tableizer.ttt_gui', 'tableizer.ttt_api', 'tableizer.ttt_email'],
    package_data={'tableizer': ['static-raw/js/*.js', 'static-raw/css/*.css', 'static-raw/img/*.png',
                   'tempates']},
    data_files=[('.', ['README.txt', 'COPYING'])],
    url="http://pypi.python.org/pypi/tableizer",
    license='GPLv2',
    description='Monitor database tables',
    long_description=open('README.txt').read(),
    install_requires=[
        'Django-dev', 
        'Pillow==2.1.0',
        'MySQL-python==1.2.4',
        'South==0.7.6',
        'humanize==0.3',
        'python-rrdtool==1.4.7',
        'djangorestframework==2.2.7',
        'Markdown==2.3.1',
        'defusedxml==0.4.1',
       ],
    setup_requires=[
       "stdeb >= 0.6",
       ],
    dependency_links=['-e git://github.com/django/django.git@20a91cce04c72bc8c64a1c43b7398edac7b709cc#egg=Django-dev'],
)
