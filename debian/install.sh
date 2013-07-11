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
export DEBIAN_FRONTEND=noninteractive
apt-get -q -y install mysql-server mysql-client 
service mysql start

# Set MySQL root password
mysqladmin -u root password "$PASSWD"

# Install libmysqlclient-dev
apt-get -y install libmysqlclient-dev

# Install Development Tools
apt-get -y install build-essential 
apt-get -y install libreadline5-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev 
apt-get -y install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev 

# Download and Install Python
cd ~
wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tgz
tar -xvf Python-2.7.3.tgz
cd Python-2.7.3
./configure --prefix=/usr/local
make && make altinstall

# Install Setuptools and Pip
cd ~
wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.36.tar.gz
tar xf distribute-0.6.36.tar.gz
cd distribute-0.6.36
python2.7 setup.py install

easy_install pip

# Install virtualenv and virtualenvwrapper
pip install virtualenv
pip install virtualenvwrapper

# Edit .bashrc file
if ! grep -F 'export WORKON_HOME=\$HOME/.virtualenvs' ~/.bashrc
then
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
fi

if ! grep -F "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7" ~/.bashrc
then
    echo "export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7" >> ~/.bashrc
fi

if ! grep -F "source /usr/local/bin/virtualenvwrapper.sh" ~/.bashrc
then
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
fi

# Reload bash
source ~/.bashrc

# Create virtualenv
mkvirtualenv --no-site-packages --distribute -p /usr/local/bin/python2.7 $VENV_NAME

# Install python-imaging
apt-get -y build-dep python-imaging 

# Fix Symlinks
if [ ! -f /usr/lib/libfreetype.so ];
then
    echo "/usr/lib/libfreetype.so not found! Created a symlink for it.";
    ln -f -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/;
fi
if [ ! -f /usr/lib/libjpeg.so ];
then
    echo "/usr/lib/libjpeg.so not found! Created a symlink for it.";
    ln -f -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
fi
if [ ! -f /usr/lib/libz.so ];
then
    echo "/usr/lib/libz.so not found! Created a symlink for it.";
    ln -f -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/;
fi

# Install Rrdtool
apt-get -y install librrds-perl rrdtool 

# Install Rrdtool-python requirements
apt-get -y install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev 
