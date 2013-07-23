#! /bin/bash

usage()
{
cat << EOF
usage: $0 options

This installs the requirements needed for Tableizer.

OPTIONS:
   -h               Show this message
   -v VENV_NAME     Name of virtualenv
   -p PASSWD        Set MySQL root password
EOF
}

VENV_NAME=
PASSWD=
while getopts “hp:v:” OPTION
do
     case $OPTION in
         h)
             usage
             exit 1
             ;;
         p)
             PASSWD=$OPTARG
             ;;
         v)
             VENV_NAME=$OPTARG
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

if [[ -z $VENV_NAME ]]
then
     echo "-v option is required."
     exit 1
fi

if [[ -z $PASSWD ]]
then
    echo "-p option is required."
    exit 1
fi

# Install and Start MySQL Server
yum install mysql mysql-server
service mysqld start

# Set MySQL root password
mysqladmin -u root password "$PASSWD"

# Install mysql-devel
yum install mysql-devel

# Install Development Tools
yum groupinstall 'Development Tools'
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel

# Download and Install Python
cd ~
wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2
tar xf Python-2.7.3.tar.bz2
cd Python-2.7.3
./configure --prefix=/usr/local
make && make altinstall

# Install Setuptools and Pip
cd ~
wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.36.tar.gz --no-check-certificate
tar xf distribute-0.6.36.tar.gz
cd distribute-0.6.36
python2.7 setup.py install

easy_install-2.7 pip

# Install virtualenv and virtualenvwrapper
pip-2.7 install virtualenv
pip-2.7 install virtualenvwrapper

# Edit .bashrc file
if ! grep -F 'export WORKON_HOME=\$HOME/.virtualenvs' ~/.bashrc
then
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
fi

if ! grep -F "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7" ~/.bashrc
then
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7" >> ~/.bashrc
fi

if ! grep - F "source /usr/local/bin/virtualenvwrapper.sh" ~/.bashrc
then
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
fi

# Reload bash
source ~/.bashrc

# Create virtualenv
mkvirtualenv --no-site-packages --distribute -p /usr/local/bin/python2.7 $VENV_NAME

# Install python-imaging and python-devel
yum install python-imaging python-devel libjpeg-devel

# Install Rrdtool
CENTOS_VERSION=$(rpm -qa \*-release | grep -Ei "oracle|redhat|centos" | cut -d"-" -f3)
UNAME=$(uname -m)

if [ $CENTOS_VERSION -eq 5 ]
then
    if [ $UNAME -eq "i386" ]
    then
        yum install perl perl-Time-HiRes ruby ruby-devel lua lua-devel xorg-x11-fonts-Type1 libdbi groff
        wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el5.rf.i386.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el5.rf.i386.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el5.rf.i386.rpm
        rpm -ivh perl-rrdtool-1.4.7-1.el5.rf.i386.rpm rrdtool-1.4.7-1.el5.rf.i386.rpm rrdtool-devel-1.4.7-1.el5.rf.i386.rpm
    elif [ $UNAME -equ "x86_64" ]
    then
        yum install perl perl-Time-HiRes ruby ruby-devel lua lua-devel xorg-x11-fonts-Type1 libdbi groff
        wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el5.rf.x86_64.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el5.rf.x86_64.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el5.rf.x86_64.rpm
        rpm -ivh perl-rrdtool-1.4.7-1.el5.rf.x86_64.rpm rrdtool-1.4.7-1.el5.rf.x86_64.rpm rrdtool-devel-1.4.7-1.el5.rf.x86_64.rpm
    else
        echo "Architecture not supported"
        exit 1
    fi
elif [ $CENTOS_VERSION -eq 6 ]
then
    if [ $UNAME -eq "i686" ]
    then
        yum install perl perl-Time-HiRes ruby xorg-x11-fonts-Type1 libdbi
        wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el6.rfx.i686.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el6.rfx.i686.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el6.rfx.i686.rpm
        rpm -ivh perl-rrdtool-1.4.7-1.el6.rfx.i686.rpm rrdtool-1.4.7-1.el6.rfx.i686.rpm rrdtool-devel-1.4.7-1.el6.rfx.i686.rpm
    elif [ $UNAME -equ "x86_64" ]
    then
        yum install perl perl-Time-HiRes ruby xorg-x11-fonts-Type1 libdbi
        wget http://pkgs.repoforge.org/rrdtool/perl-rrdtool-1.4.7-1.el6.rfx.x86_64.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-1.4.7-1.el6.rfx.x86_64.rpm
        wget http://pkgs.repoforge.org/rrdtool/rrdtool-devel-1.4.7-1.el6.rfx.x86_64.rpm
        rpm -ivh perl-rrdtool-1.4.7-1.el6.rfx.x86_64.rpm rrdtool-1.4.7-1.el6.rfx.x86_64.rpm rrdtool-devel-1.4.7-1.el6.rfx.x86_64.rpm
    else
        echo "Architecture not supported"
        exit 1
    fi
else
    echo "CentOS Version not supported"
    exit 1
fi

# Install Rrdtool-python requirements
yum install cairo-devel libxml2-devel pango pango-devel libpng-devel freetype freetype-devel libart_lgpl-devel

