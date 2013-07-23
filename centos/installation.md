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

    yum groupinstall 'Development Tools'
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
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7
    source /usr/local/bin/virtualenvwrapper.sh

#### Reload bash

    source ~/.bashrc

#### Create Virtualenv

    mkvirtualenv --no-site-packages --distribute -p /usr/local/bin/python2.7 mysql_tools

## Install Python-imaging and Python-devel

    yum install python-imaging python-devel libjpeg-devel

## Install Rrdtool

For CentOS 5, 32-bit,

    yum install perl perl-Time-HiRes ruby ruby-devel lua lua-devel xorg-x11-fonts-Type1 libdbi groff
    wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el5.rf.i386.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el5.rf.i386.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el5.rf.i386.rpm
    rpm -ivh perl-rrdtool-1.4.7-1.el5.rf.i386.rpm rrdtool-1.4.7-1.el5.rf.i386.rpm rrdtool-devel-1.4.7-1.el5.rf.i386.rpm
    
For CentOS 5, 64-bit,

    yum install perl perl-Time-HiRes ruby ruby-devel lua lua-devel xorg-x11-fonts-Type1 libdbi groff
    wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el5.rf.x86_64.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el5.rf.x86_64.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el5.rf.x86_64.rpm
    rpm -ivh perl-rrdtool-1.4.7-1.el5.rf.x86_64.rpm rrdtool-1.4.7-1.el5.rf.x86_64.rpm rrdtool-devel-1.4.7-1.el5.rf.x86_64.rpm
    
For CentOS 6, 32-bit,

    yum install perl perl-Time-HiRes ruby xorg-x11-fonts-Type1 libdbi
    wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el6.rfx.i686.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el6.rfx.i686.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el6.rfx.i686.rpm
    rpm -ivh perl-rrdtool-1.4.7-1.el6.rfx.i686.rpm rrdtool-1.4.7-1.el6.rfx.i686.rpm rrdtool-devel-1.4.7-1.el6.rfx.i686.rpm
    
For CentOS 6, 64-bit,
    
    yum install perl perl-Time-HiRes ruby xorg-x11-fonts-Type1 libdbi
    wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el6.rfx.x86_64.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el6.rfx.x86_64.rpm
    wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el6.rfx.x86_64.rpm
    rpm -ivh perl-rrdtool-1.4.7-1.el6.rfx.x86_64.rpm rrdtool-1.4.7-1.el6.rfx.x86_64.rpm rrdtool-devel-1.4.7-1.el6.rfx.x86_64.rpm

#### Rrdtool-python requirements

    yum install cairo-devel libxml2-devel pango pango-devel libpng-devel freetype freetype-devel libart_lgpl-devel

