#Sqlcanon
- is a tool that canonicalizes statements read from either log files, stdin or captured packets.

When applicable (especially when reading from log files) it also extracts additional data found and saved for reporting purposes.

Currently it has two parts: sqlcanonclient and sqlcanon server.  Sqlcanonclient is the one responsible for canonicalizing and extracting data. It has the option to pass data to sqlcanon server (in client-server mode) or just store them locally (stand-alone mode).

Current Features:

* Process MySQL slow query log
* Process MySQL general query log
* Process statements from captured packets
* Process statements from stdin
* Captured statements are stored as RRD.

See docs/sqlcanon.md for more information.

#Tableizer
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
