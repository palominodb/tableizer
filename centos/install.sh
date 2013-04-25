#! /bin/bash

usage()
{
cat << EOF
usage: $0 options

This installs the requirements needed for MySQL Tools.

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
yum groupinstall “Development tools”
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

# Install python-imaging
yum install python-imaging

# Install Rrdtool
CENTOS_VERSION=$(rpm -qa \*-release | grep -Ei "oracle|redhat|centos" | cut -d"-" -f3)

if [ $CENTOS_VERSION -eq 5 ]
then
    rpm -ivh http://apt.sq.be/redhat/el5/en/i386/rpmforge/RPMS/rpmforge-release-0.5.2-2.el5.rf.i386
    yum install rrdtool -y
elif [ $CENTOS_VERSION -eq 6 ]
then
    rpm -ivh http://apt.sw.be/redhat/el6/en/i386/rpmforge/RPMS/rpmforge-release-0.5.2-2.el6.rf.i686.rpm
    yum install rrdtool -y
else
    echo "CentOS Version not supported"
    exit 1
fi

# Install Rrdtool-python requirements
yum install cairo-devel libxml2-devel pango-devel libpng-devel freetype-devel libart_lgpl-devel

# Install libpcap
yum install libpcap libpcap-devel

