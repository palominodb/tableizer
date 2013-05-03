# Debian Setup

*Note: You may need to run some of the commands as root.*

## Install and start MySQL

    apt-get install mysql-server mysql-client
    service mysql start
    
    # PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
    # To do so, start the server, then issue the following commands:
    mysqladmin -u root password 'new-password'
    
## Install libmysqlclient-dev

    apt-get install libmysqlclient-dev

You may need to install Python2.7 if you're Ubuntu ships a different version.

## Install Python 2.7

#### Development Tools

    apt-get install build-essential
    apt-get install libreadline5-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    
If the above command don't work, try

    apt-get install build-essential
    apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
    
#### Download and install Python

    cd ~
    wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tgz
    tar -xvf Python-2.7.3.tg
    cd Python-2.7.3
	./configure --prefix=/usr/local
	make && make altinstall
    
## Install Setuptools and Pip

    cd ~
    wget http://pypi.python.org/packages/source/d/distribute/ditstribute-0.6.36.tar.gz
    tar xf distribute-0.6.36.tar.gz
	cd distribute-0.6.36
	python2.7 setup.py install

	easy_install pip
    
## Virtualenv and Virtualenvwrapper

    pip install virtualenv
    pip install virtualenvwrapper

#### Edit your .bashrc file and add the following lines

    export WORKON_HOME=$HOME/.virtualenvs
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7
    source /usr/local/bin/virtualenvwrapper.sh

#### Reload bash

    source ~/.bashrc

#### Create Virtualenv

    mkvirtualenv --no-site-packages --distribute -p /usr/local/bin/python2.7 mysql_tools

## Install Build Dependencies

    apt-get build-dep python-imaging
    
### Fix Symlinks

    ln -f -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    ln -f -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    ln -f -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

## Install Rrdtool

    apt-get install librrds-perl rrdtool

#### Rrdtool-python requirements

    apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev
