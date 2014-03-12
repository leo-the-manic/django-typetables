django-typetables
-----------------
**NOT CURRENTLY SUITABLE FOR USE. NOT COMPLETE. UNDER DEVELOPMENT.**

Database-backed enumerations for Django.


Summary
```````
Use the ``@typetable.typetable`` decorator on a class. This class should have
a standard auto-incrementing primary key column.

Add ``typetable.Value``` attributes to the class. These must specify an
integer primary key, as well as whatever other value types that are desired.

Run a currently unimplemented "installation" command which will generate the
database rows specified in your typetable class.

When you need to change a typetable value, perform the change in code then
run a currently unimplemented command to generate an appropriate data
migration.
