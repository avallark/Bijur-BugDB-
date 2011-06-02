*** Bijur BUGDB ***

** License ** 

GPL v3 : refer to gpl.txt

** Requirements ** 

Flask : http://flask.pocoo.org/

Python 2.7 (Am pretty sure it works on 2.5+)

MySQL server 5.3+

** Python Module requirements: **

MySQLdb (http://sourceforge.net/projects/mysql-python/)


** How to install and run **

Connect to DB on mysql and create the schema using the file schema.sql:

mysql --user=<MYSQLUSERNAME> -p -D >MYSQLDATABASENAME> < schema.sql

You can make changes to schema.sql but only for the STATUSes in the insert statements.

First edit the db.py file to include your own mysql database, user and password. Currently its set to tasks/tasks12@tasksdb

Then run the below from a shell
$ python tasks.py


** TODO **

Todo is a list of things I hope to add in the next release and does not really include the complete to-do list

1. Categories and subcategories of bugs.
2. Archive bugs.
3. Report to show how many bugs were logged, solved in the past one week, month.


** ChangeLog **

02 - 06 - 2011

Added notification everytime a bug is assigned to the user. Notifications cannot be currently disabled. 

29 - 05 - 2011

Have added a configurations page which will now let you configure default statuses. And also see the debug messages.


25-03-2011

First Commit to Git. Also cleaned up the code a little bit.
