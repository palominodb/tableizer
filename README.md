# Tableizer
*This tool is a python port of the table-tracking-toolkit gem(https://github.com/palominodb/PalominoDB-Public-Code-Repository/tree/master/tools/table_tracking). This tool also contains a port of the pdb-dsn gem which is being used to parse the pdb-dsn file.*

## Contents

1. Overview
2. Getting Started
3. Examples

### Overview

Tableizer allows simple collecting and detailed reporting on:
- Table schema changes (tracking 'show create table' changes over time)
- Table volume-metrics (tracking table size over time)
- Table user permission changes (tracking changes on user privs)

TTT has a pluggable system for implementing new metrics which could be used to track other things like "SHOW STATUS".

TTT also has a pluggable reporting/querying interface which out of the box support for generating reports suitable for:
- text viewing ( in the moment troubleshooting, see when it went wrong )
- email ( being kept apprise of developer madness )
- nagios ( being alerted of developer madness )
- rrdtool

### Getting Started

If you're going to use rrdtool, you need to execute this command first.

`sudo apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev rrdtool`

1. Create a virtual environment. *Note: You need to install [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/). When creating a virtualenv you may need to pass --no-site-packages.*

    `mkvirtualenv tableizer`
    
2. Install the requirements

    `pip install -r requirements.txt`
    
3. Configure your local_settings.py, config.yml and dsn.yml. An example of a local_settings.py, config.yml, and a dsn.yml are included in the distribution. The local_settings.py file should be placed in the same deirectory as the settings.py

4. You will also need an sql user to do the data collection. It is Highly recommended that you make a user just for ttt, for both security and accountability purposes. TTT needs 'select', and 'show view' priviliges. The below query give the 'ttt' user the appropriate permissions.

   `GRANT SELECT, SHOW VIEW ON *.* TO 'ttt'@'ops.example.com' IDENTIFIED BY 'password'`
   
### Examples
For best results 'ttt-collect' should be run daily or every N hours. Running it or 'ttt-query' with '--help', or '-h', will show usage information.

In general, though, your 'ttt-collect' commandline will be:
    `./manage.py ttt-collect --config config.yml --dsn dsn.yml`
    or
    `./manage.py ttt-collecto -c config.yml -d dsn.yml`

That should be put in a crontab and run as often as you feel like.

To be emailed of any table changes that happen:
    `./manage.py ttt-query --config config.yml --stat definition --since last`

The report generated shows you what happened with the most recent 'version'  of each table. The output is: "compare the most recent entry with the previous". For table definitions, only changes are stored, so, if a new table was created and then never altered, it will always show up as 'new' in that query.

It's a useful display, but often it's better to use --since to prune any changes older than a certain age. For example, if you run the collector every 4 hours, then running this query would probably be more interesting:
    `./manage.py ttt-query --config config.yml --stat definition --since 4h`
    
Which will only show 'new' tables in the 4 hour window that they showed up in.

Volumetrics are collected every time, regardless of changes. This is to support export to rrd and other tools.
    `./manage.py ttt-query --config config.yml --stat volume --order 'data_length,-index_length' --limit 50`
    
This will show you the top 50 tables ordered by size after doing 'ignore tables' handling. To report on all tables add '--raw' to the commandline.
    
