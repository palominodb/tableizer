# CentOS Setup

*Note: You may need to run some of the commands as root.*

## Install and start MySQL

    yum install mysql mysql-server
    service mysqld start
    
    # PLEASE REMEMBER TO SET A PASSWORD FOR THE MySQL root USER !
    # To do so, start the server, then issue the following commands:
    mysqladmin -u root password 'new-password'

## Install mysql-devel

    yum install mysql-devel

You may need to install Python2.7 if you're CentOS ships a different version.

## Install Python 2.7

#### Development Tools

    yum groupinstall “Development tools”
    yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel
    
#### Download and install Python

    cd ~
    wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
    tar xf Python-2.7.3.tar.bz2
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

## Install Python-imaging

    yum install python-imaging

## Install Rrdtool

For CentOS 5,

    rpm -ivh http://apt.sq.be/redhat/el5/en/i386/rpmforge/RPMS/rpmforge-release-0.5.2-2.el5.rf.i386
    yum install rrdtool -y
    
For CentOS 6,

    rpm -ivh http://apt.sw.be/redhat/el6/en/i386/rpmforge/RPMS/rpmforge-release-0.5.2-2.el6.rf.i686.rpm
    yum install rrdtool -y

#### Rrdtool-python requirements

    yum install cairo-devel libxml2-devel pango-devel libpng-devel freetype-devel libart_lgpl-devel

## Install libpcap

    yum install libpcap libpcap-devel

