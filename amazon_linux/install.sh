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

# Install gcc
yum install gcc
yum install gcc-c++
yum install make

# Install and Start MySQL Server
yum install mysql mysql-server
service mysqld start

# Set MySQL root password
mysqladmin -u root password "$PASSWD"

# Install mysql-devel
yum install mysql-devel

# Install Python
yum install python27
yum install python-devel python27-devel

# Install Setuptools and Pip
cd ~
wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.36.tar.gz
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

if ! grep -F "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7" ~/.bashrc
then
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7" >> ~/.bashrc
fi

if ! grep - F "source /usr/local/bin/virtualenvwrapper.sh" ~/.bashrc
then
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
fi

# Reload bash
source ~/.bashrc

# Create virtualenv
mkvirtualenv --no-site-packages --distribute -p /usr/bin/python2.7 $VENV_NAME

# Install python-imaging
yum install python-imaging libjpeg-devel

# Install rrdtool
yum install rrdtool rrdtool-devel

# Install rrdtool-python requirements
yum install cairo-devel libxml2-devel pango-devel libpng-devel freetype freetype-devel libart_lgpl-devel
