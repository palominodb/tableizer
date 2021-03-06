# Amazon Linux Setup

*Note: You may need to run some of the commands as root.*

## Install gcc

    yum install gcc
    yum install gcc-c++
    yum install make

## Install and start MySQL

    yum install mysql mysql-server
    service mysqld start
    
    # PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
    # To do so, start the server, then issue the following commands:
    mysqladmin -u root password 'new-password'

## Install mysql-devel

    yum install mysql-devel

You may need to install Python2.7 if you're Amazon Linux ships a different version.

## Install Python 2.7

    yum install python27
    yum install python-devel python27-devel
    
## Install Setuptools and Pip

    cd ~
    wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.36.tar.gz
    tar xf distribute-0.6.36.tar.gz
	cd distribute-0.6.36
	python2.7 setup.py install

	easy_install-2.7 pip
    
## Virtualenv and Virtualenvwrapper

    pip-2.7 install virtualenv
    pip-2.7 install virtualenvwrapper
    
#### Edit your .bashrc file and add the following lines

    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7
    source /usr/bin/virtualenvwrapper.sh


#### Reload bash

    source ~/.bashrc

#### Create Virtualenv

    mkvirtualenv --no-site-packages --distribute -p /usr/bin/python2.7 mysql_tools

## Install Python-imaging

    yum install python-imaging libjpeg-devel

## Install Rrdtool

    yum install rrdtool rrdtool-devel

#### Rrdtool-python requirements

    yum install cairo-devel libxml2-devel pango-devel libpng-devel freetype freetype-devel libart_lgpl-devel
