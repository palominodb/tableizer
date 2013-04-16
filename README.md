*Documentation for MySQL Tools and SQLCanon client.*

#MySQL Tools
*This is a collection of tools for monitoring MySQL.*

##Contents
1. Overview
2. Requirements installation
3. Getting Started
4. Usage

## Overview
###Sqlcanon
- is a tool that canonicalizes statements read from either log files, stdin or captured packets.

When applicable (especially when reading from log files) it also extracts additional data found and saved for reporting purposes.

Currently it has two parts: sqlcanonclient and sqlcanon server.  Sqlcanonclient is the one responsible for canonicalizing and extracting data. It has the option to pass data to sqlcanon server (in client-server mode) or just store them locally (stand-alone mode).

Current Features:

- Process MySQL slow query log
- Process MySQL general query log
- Process statements from captured packets
- Process statements from stdin
- Captured statements are stored as RRD.

###Tableizer
- is a python port of the table-tracking-toolkit gem(https://github.com/palominodb/PalominoDB-Public-Code-Repository/tree/master/tools/table_tracking).

Tableizer allows simple collecting and detailed reporting on:
- Table schema changes (tracking 'show create table' changes over time)
- Table volume-metrics (tracking table size over time)
- Table user permission changes (tracking changes on user privs)

Tableizer has a pluggable system for implementing new metrics which could be used to track other things like "SHOW STATUS".

Tableizer also has a pluggable reporting/querying interface which out of the box support for generating reports suitable for:
- text viewing ( in the moment troubleshooting, see when it went wrong )
- email ( being kept apprise of developer madness )
- nagios ( being alerted of developer madness )
- rrdtool

## Installation(Building your environment)

Requirements:
- Python 2.7
- Pip
- Virtualenv
- Virtualenvwrapper
- Python-imaging
- Rrdtool
- Libpcap

If you are using Debian, you can follow the steps at debian/installation.md. Moreover, you can execute debian/install.sh to automate installations.
On the otherhand, if you are using CentOS, you can follow the steps at centos/installation.md. Moreover, you can execute centos/install.sh to automate installations.

### install.sh
    usage: ./install.sh options

    This installs the requirements needed for MySQL Tools.
    
    OPTIONS:
       -h               Show this message
       -v VENV_NAME     Name of virtualenv
       -p PASSWD        Set MySQL root password


## Getting Started
1. Activate your virtualenv

        workon <venv_name>
    
2. Install MySQL Tools requirements

        cd <src_dir>/mysql_tools
        pip install -r requirements.txt
    
3. Rename local_settings.py.template to local_settings.py. Configure your local_settings.py file. (See Setting section for more detailed discussion)

4. You will also need an sql user to do the data collection. It is Highly recommended that you make a user just for tableizer, for both security and accountability purposes. MySQL Tools needs 'select', and 'show view' priviliges. The below query give the 'mysql_tools' user the appropriate permissions.

        GRANT SELECT, SHOW VIEW ON *.* TO 'mysql_tools'@'ops.example.com' IDENTIFIED BY 'password';

5. Create MySQL Tools database

    In your MySQL console,
    
        CREATE DATABASE mysql_tools;

6. Run syncdb

        ./manage.py syncdb

7. Run the migrations

        ./manage.py migrate

8. Start the built-in server

        ./manage.py runserver
        
    *Note: You can also host MySQL Tools using webservers like Apache and Nginx.*
    
### Settings
In the mysql_tools directory, you will find two settings file; settings.py and local_settings.py. This is good if you want to install mysql_tools in different hosts. The settings.py file will contain the settings similar settings across all installations and default values. On the other hand, the local_settings.py file allows you to override defaults and global settings.

#### MySQL Tools-specific settings

1. DATABASES - MySQL Tools takes advantage of Django's multi-DB support. In the example below, the settings must always have a 'default' database. This is the database that will be used by mysql_tools to store results from data collection.
    
    ###### Adding hosts
    The other datatabase configurations in the settings will contain the settings for the hosts where you want data to be collected. The template below can be used to add hosts.

    TEMPLATE:

        '<hostname>_information_schema': {
            'ENGINE': 'django.db.backends.mysql', 
            'NAME': 'information_schema', 
            'USER': 'user',
            'PASSWORD': 'password',
            'HOST': '<hostname>',
            'PORT': '',
        }
    
    ###### Sample DATABASES setting

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
                'NAME': 'tableizer',                      # Or path to database file if using sqlite3.
                'USER': 'user',                      # Not used with sqlite3.
                'PASSWORD': 'password',                  # Not used with sqlite3.
                'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
            },
            'localhost_information_schema': {
                'ENGINE': 'django.db.backends.mysql', 
                'NAME': 'information_schema', 
                'USER': 'user',
                'PASSWORD': 'password',
                'HOST': 'localhost',
                'PORT': '',
            },
        }

2. REPORT_IGNORE - This is a list of regexes to ignore during reporting
    
        REPORT_IGNORE = {
            'global': (
                'mysql\..*',
            ),
            'volume': (
                'nogrowthdb\..*',
            ),
        }

3. SEND_CRASHREPORTS - Send Crash Reports to PalominoDB. (To-do)

4. REPORT_OPTIONS - Options for reporting when using text output
        
        REPORT_OPTIONS = {
            'display_with': 135,
            'full': False,
        }

5. FORMATTER_OPTIONS - Output formatting options
    
        
        FORMATTER_OPTIONS = {
            # This formatter exports to RRD.
            # Presently, it IGNORES all query options, and simply
            # updates RRD in a fixed format. This may be changed at a later time.
            # The RRD formatter also does not store create syntax changes right now
            # Extending it to do so should be trival, but seemed less important than
            # volumetrics for the first release.
            # The 'path' option specifies where to write out RRDs.
            # It should be an absolute path.
            # RRD is sensitive to time, if you are going to export to RRD
            # you must be prepared to run the RRD export on a regular basis.
            # If you are just simply looking to generate some "one-time" graphs,
            # The RRD exporter DOES insert old entries, so you can simple run it,
            # and do whatever graph creation you want.
            'rrd': {
                'path': '/tmp/rrd',
                # This is needed so RRD knows "how often" you'll be feeding results to it.
                # This is only used during RRD creation time, after that, if you wait
                # longer to update the rrd, this formatter will fill in all intervening
                # entries. Additionally, if you change this after RRDs have been created,
                # only new rrds will pickup the change.
                # Syntax is: X[hmd], where 'h' is hours, 'm' is minutes, and 'd' is days
                # There is a maximum of two days for any interval.
                'update_interval': '10m',
            },
            'nagios': {
                # One of 'critical', 'warning', 'unknown', 'ok'
                # Defines how the formatter should treat
                # changes to the monitored tables
                # The default level is 'warning'
                'alert_level': 'warning',
                # Table regexes to alert on. This is an inclusion mechanism
                # as opposed to an exclusion mechanism. Tables that you wish
                # to recieve nagios alerts for must be included by one of your regexes.
                # It's recommended to make these as specific as reasonable.
                'tables':(
                    '.*',
                )
            },
            # This formatter is designed for emailing periodic reports.
            # Emailing one-time reports should probably be done by using the
            # 'text' formatter, and piping the output to the `mail` command.
            'email': {
                'subjectprefix': '[MySQL Tools] ',
                'emailto': 'email@email.com',
                # Whether or not to send emails with no changes.
                'send_empty': False,
                # This can be 'sendmail' or 'smtp'
                # Defaults to 'sendmail'
                'delivery_method': 'smtp',
                'sendmail_settings': {
                    'location': '/usr/sbin/sendmail'
                },
                'smtp_settings': {
                    'host': 'smtp.gmail.com',
                    'port': 587,
                    'user': 'email@email.com',
                    'password': 'password',
                    'use_tls': True,
                },
            }
        }

## Usage

### MySQL Tools management commands

1. tableizer-collect - This is the command for data collection. For best results, this command should be run daily or every N hours.
        
    To collect all statistics,
        
        ./manage.py tableizer-collect

    To collect specific statistics(eg. definition),
        
        ./manage.py tableizer-collect --stat definition
        
    To list available statistics,
    
        ./manage.py tableizer-collect --list-stats
        
    For more command options,
    
        ./manage.py tableizer-collect --help

2. tableizer-query - This is the command for data reporting. The available output modes are:
        - text (all statistics are available)
        - email (available statistics: definition, view, user)
        - nagios (all statistics are available)
        - rrd (available statistics: volume)

    To report statistics(the default statistic to be reported is definition),
        
        ./manage.py tableizer-query
        
    To report specific statistic,
    
        ./manage.py tableizer-query --stat volume
    
    For more command options,
    
        ./manage.py tableizer-query --help
        
    *Note: The GUI shows graphs generated from rrds created by the tableizer-query command. For best results you should also add the tableizer-query command with output mode set to rrd to your crontab. When tested, the rrds need at least three consecutive data points to generate a useful graph.*
    
3. tableizer-admin - This is the command for performing some admin functions.
    
    To list available hosts,

        ./manage.py tableizer-admin list

    To rename a host,
        
        ./manage.py tableizer-admin rename old_host_name new_host_name
        
    To purge a host,
    
        ./manage.py tableizer-admin purge host_name
        
    For more command options,
        
        ./manage.py tableizer-admin --help

# SQLCanon Client

## Contents
1. Installation
2. Usage
3. Configuration
4. Examples
5. Utilities

## Install SQLCanon client requirements

    workon <venv_name>
    cd <src_dir>/sqlcanonclient/src/sqlcanonclient
    pip install -r requirements.txt
    
## Usage    

    usage: sqlcanonclient.py [-h] [-t {s,g}] [-d DB] [-s]
                     [--server-base-url SERVER_BASE_URL]
                     [--save-statement-data-path SAVE_STATEMENT_DATA_PATH]
                     [--save-explained-statement-path SAVE_EXPLAINED_STATEMENT_PATH]
                     [-e EXPLAIN_OPTIONS]
                     [-l | --local-run-last-statements | --print-top-queries PRINT_TOP_QUERIES]
                     [--sliding-window-length SLIDING_WINDOW_LENGTH]
                     [-i INTERFACE] [-f FILTER] [--encoding ENCODING]
                     [--encoding-errors {strict,ignore,replace}]
                     [-S SERVER_ID] [-C CONFIG] [--no-skip-unknowns]
                     [file]

    positional arguments:
      file                  MySQL log file to open, if not specified stdin will be
                            used. (default: None)
    
    optional arguments:
      -h, --help            show this help message and exit
      -t {s,g}, --type {s,g}
                            Log file format -- s: slow query log, g: general query
                            log (default: s)
      -d DB, --db DB        database name (default: /tmp/sqlcanonclient.db)
      -s, --stand-alone     Run as stand alone (will not send data to server).
                            (default: False)
      --server-base-url SERVER_BASE_URL
                            Server base URL. (default: http://localhost:8000)
      --save-statement-data-path SAVE_STATEMENT_DATA_PATH
                            URL to be used for saving statement data. (default:
                            /canonicalizer/save-statement-data/)
      --save-explained-statement-path SAVE_EXPLAINED_STATEMENT_PATH
                            URL to be used for saving explain statement. (default:
                            /canonicalizer/save-explained-statement/)
      -e EXPLAIN_OPTIONS, --explain-options EXPLAIN_OPTIONS
                            Explain MySQL options:
                            [h=<host>][,P=<port>][,u=<user>][,p=<passwd>][,d=<db>]
                            (default: h=127.0.0.1)
      -l, --sniff           launch packet sniffer (default: False)
      --local-run-last-statements
                            In stand alone mode, prints last seen statements
                            (default: False)
      --print-top-queries PRINT_TOP_QUERIES
                            Prints top queries stored on local data. (default: 0)
      --sliding-window-length SLIDING_WINDOW_LENGTH
                            Length of period in number of minutes. (default: 5)
      -i INTERFACE, --interface INTERFACE
                            interface to sniff from (default: lo0)
      -f FILTER, --filter FILTER
                            pcap-filter (default: dst port 3306)
      --encoding ENCODING   String encoding. (default: utf_8)
      --encoding-errors {strict,ignore,replace}
                            String encoding error handling scheme. (default:
                            replace)
      -S SERVER_ID, --server-id SERVER_ID
                            Server ID. (default: 1)
      -C CONFIG, --config CONFIG
                            Name of configuration file to use. (default:
                            ./config.yml)
      --no-skip-unknowns    Any value other than 0 will skip processing of non
                            DDL/DML statements. (default: False)
                            
## Configuration
If you specify a configuration file via `-C` or `--config`, the values from the file will be load and will override the values from the command line arguments. You have to use the longer versions of the option names and convert dashes into underscores in the configuration file. The following is a sample content:

    # input file, if not specified, stdin will be used instead
    file: /var/log/mysql/mysql-slow.log
    
    # contents of input file
    # values: s|g
    #   s - MySQL slow query log
    #   g - MySQL general query log
    type: s
    
    # Local sqlite3 database, used in stand-alone mode
    db: /tmp/sqlcanonclient.db
    
    # Run in stand_alone mode?
    stand_alone: False
    
    # Server base url, used when not in stand-alone mode
    server_base_url: http://localhost:8000
    
    # Server paths: save statement
    save_statement_data_path: /canonicalizer/save-statement-data/
    
    # Server paths: save explained statement
    save_explained_statement_path: /canonicalizer/save_explained_statement_path/
    
    # DSN to be used when executing EXPLAIN statements in the form:
    # h=<host>,u=<user>,p=<passwd>,d=<db>
    explain_options: h=127.0.0.1
    
    # Run packet sniffer?
    sniff: False
    
    # Interface to listen to, when running packet sniffer.
    interface: lo0
    
    # An pcap-filter expression used to filter packets.
    # The default 'dst port 3306' will suffice to for listening packets with destination port 3306.
    filter: dst port 3306
    
    # Run a sliding window of last statements? (requires stand_alone=True)
    local_run_last_statements: False
    
    # The value specified here is in minutes and is used with local_run_last_statements option.
    # A value of 5 means 'display statements found in the last 5 minutes'.
    sliding_window_length: 5
    
    # The value N used to print top N queries. (requires stand_alone=True if N > 0)
    print_top_queries: 0
    
    # String encoding
    # default: utf_8
    encoding: utf_8
    
    # String encoding error handling scheme.
    # values: strict|ignore|replace
    encoding_errors: replace
    
    # Server ID
    server_id: 1

## Examples

### Processing MySQL slow query log
#### Client-server mode:

    ./sqlcanonclient.py /var/log/mysql/mysql-slow.log
    
The above command will process the contents of the specified slow query log and will send data to the sqlcanon server using the default --server-base-url value. If you specified ipaddr:port option when running sqlcanon server, you need to provide this to the sqlcanon client using --server-base-url.
In client-server mode, sqlcanonclient will not attempt to save data locally, it will instead pass it to the sqlcanon server.  When sqlcanon server receives data it will ask sqlcanonclient to run an EXPLAIN for statements that were seen for the first time.  The sqlcanon will run EXPLAIN using the connection options specified in --explain-options. The resulting rows will be sent to and stored by the sqlcanon server.

#### Stand-alone mode:
In stand-alone mode you simply use -s option and optionally the name of the sqlite database to be used for storing data locally.
    
    ./sqlcanonclient.py -s -d ./data.db /var/log/mysql/mysql-slow.log
    
    # from stdin variation
    cat /var/log/mysql/mysql-slow.log | ./sqlcanonclient.py -s -d ./data.db
    
#### Viewing data in stand-alone mode:
Current data views present on sqlcanon client are last statements seen and top queries:

    # continously display last seen statements for the last 5 minutes (usually ran under on another terminal window)
    ./sqlcanonclient.py -s -d ./data.db --local-run-last-statements --sliding-window-length 5
    
    # print top 5 queries (based on the count of canonicalized statement-hostname hash, in descending order)
    ./sqlcanonclient.py -s -d ./data.db --print top-queries 5

Currently sqlcanonclient has no capability to display rows stored on local tables.
To check locally stored data, you can use sqlite3 to open the db file.

### Processing MySQL general query log

Client-server mode:

    ./sqlcanonclient.py -t g /var/log/mysql/mysql.log

Stand-alone mode:

    ./sqlcanonclient.py -s -d ./data.db -t g /var/log/mysql/mysql.log
    
    # from stdin variation
    cat /var/log/mysql/mysql.log | ./sqlcanonclient.py -s -d ./data.db -t g
    
### To read statements from captured packets

    # sqlcanonclient needs user with privilege to capture packet data to run sniffer.
    # Listen from interface 'lo' (loopback)
    ./sqlcanonclient.py -l -i lo
    # On another terminal, connect a mysql client to test capture
    # Client was listening on lo interface, connect mysql client to loopback address
    mysql -h 127.0.0.1
    
    # Listen from interface 'eth0', filter packets by destination port 3306
    ./sqlcanonclient.py -l -i eth0 -f dst port 3306
    mysql -h 192.168.2.101
    
### Running Unit Tests

    cd <src_dir>/sqlcanonclient/src/sqlcanonclient
    python -m unittest -v tests
    
## Utilities

### dosql.py

#### Usage

    usage: dosql.py [-h] [-H HOST] [-P PORT] [-u USER] [-p PASSWD] [-d DB]
                    {inserts,selects}
    
    positional arguments:
      {inserts,selects}     method to run.
    
    optional arguments:
      -h, --help            show this help message and exit
      -H HOST, --host HOST  db host (default: localhost)
      -P PORT, --port PORT  db port (default: None)
      -u USER, --user USER  db user (default: sandbox)
      -p PASSWD, --passwd PASSWD
                            db password (default: sandbox)
      -d DB, --db DB        db name (default: sandbox)
    
*Sample Usage*

    # Perform inserts
    ./dosql.py -H localhost -u sandbox -p sandbox -d sandbox inserts
    
    # Perform selects
    ./dosql.py -H localhost -u sandbox -p sandbox -d sandbox selects
