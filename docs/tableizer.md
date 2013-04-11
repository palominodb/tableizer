# Tableizer
*This tool is a python port of the table-tracking-toolkit gem(https://github.com/palominodb/PalominoDB-Public-Code-Repository/tree/master/tools/table_tracking).*

## Contents

1. Overview
2. Getting Started
3. Settings
4. Management Commands
5. The GUI

### Overview

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

### Getting Started

1. Install rrdtool

`sudo apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev rrdtool`

2. Create a virtual environment. *Note: You need to install [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/). When creating a virtualenv you may need to pass --no-site-packages.*

    `mkvirtualenv tableizer`
    
    For succeeding usage, you need to activate the virtualenv.
    
    `workon tableizer`
    
3. Install the requirements

    `pip install -r requirements.txt`
    
4. Rename local_settings.py.template to local_settings.py. Configure your local_settings.py file. (See Setting section for more detailed discussion)

5. You will also need an sql user to do the data collection. It is Highly recommended that you make a user just for tableizer, for both security and accountability purposes. Tableizer needs 'select', and 'show view' priviliges. The below query give the 'tableizer' user the appropriate permissions.

   `GRANT SELECT, SHOW VIEW ON *.* TO 'tableizer'@'ops.example.com' IDENTIFIED BY 'password';`

5. Create Tableizer database

    `CREATE DATABASE tableizer;`
    
6. Run syncdb

    `./manage.py syncdb`

7. Run the migrations

    `./manage.py migrate`
    
### Settings

In the tableizer directory, you will find two settings file; settings.py and local_settings.py. This is good if you want to install tableizer in different hosts. The settings.py file will contain the settings similar settings across all installations and default values. On the other hand, the local_settings.py file allows you to override defaults and global settings.

####Tableizer-specific settings

1. DATABASES - Tableizer takes advantage of Django's multi-DB support. In the example below, the settings must always have a 'default' database. This is the database that will be used by tableizer to store results from data collection.
    
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
                'subjectprefix': '[Tableizer] ',
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

### Management Commands

1. tableizer-collect - This is the command for data collection. For best results, this command should be run daily or every N hours.
        
    To collect all statistics,
        `./manage.py tableizer-collect`

    To collect specific statistics(eg. definition),
        `./manage.py tableizer-collect --stat definition`
        
    To list available statistics,
        `./manage.py tableizer-collect --list-stats`
        
    For more command options,
        `./manage.py tableizer-collect help`

2. tableizer-query - This is the command for data reporting. The available output modes are:
        - text (all statistics are available)
        - email (available statistics: definition, view, user)
        - nagios (all statistics are available)
        - rrd (available statistics: volume)

    To report statistics(the default statistic to be reported is definition),
        `./manage.py tableizer-query`
        
    To report specific statistic,
        `./manage.py tableizer-query --stat volume`
    
    For more command options,
        `./manage.py tableizer-query help`
        
    *Note: The GUI shows graphs generated from rrds created by the tableizer-query command. For best results you should also add the tableizer-query command with output mode set to rrd to your crontab. When tested, the rrds need at least three consecutive data points to generate a useful graph.*
    
3. tableizer-admin - This is the command for performing some admin functions.
    
    To list available hosts,
        `./manage.py tableizer-admin list`

    To rename a host,
        `./manage.py tableizer-admin rename old_host_name new_host_name`
        
    To purge a host,
        `./manage.py tableizer-admin purge host_name`
        
    For more command options,
        `./manage.py tableizer-admin help`
    
### The GUI

To run the GUI, you can either setup apache and host the webapp or you can use Django's built-in development server.
    `./manage.py runserver`
