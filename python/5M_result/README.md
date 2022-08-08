# Here is a short result

Database    |avg time  | 99% time | QPS    | disk usage   | memory usage|  CPU load
--------    | -------  | -------- | ------ | ------------ | ----------  | ---------
python only | 4.276ms  | 13ms     | 935.39 | N/A         | N/A         | N/A
redis       | 7.978ms  | 18ms     | 501.35 | 0.5G         | 750MB      | 0.7
mongodb     | 8.414ms  | 18ms      | 475.42 | 0.5G         | 576MB       | 0.7
mariadb-asgi     | 20.013ms  | 81ms     | 199.87 | 2.1G         | 640MB      | 1.7
mariadb-wsgi     | 8.079ms  | 17ms     | 495.08 | 2.1G         | 490MB      | 1.6
postgresql-asgi  | 25.810ms | 47ms     | 154.98 | 1.8G         | 1200MB      | 3.2
postgresql-wsgi  | 8.429ms | 14ms     | 474.54 | 1.8G         | 545MB      | 1.3
cassandra   | 9.652ms  | 20ms     | 414.41 | 1.0G         | 500MB      | 1.0
python-pypy   | 1.496ms  | 5ms     | 2673.05 | N/A        | N/A      | N/A
postgresql-wsgi-pypy  | 8.746ms | 16ms     | 457.36 | 1.8G         | 545MB      | 1.3
mongodb-pypy     | 6.242ms  | 14ms      | 640.86 | 0.5G         | 576MB       | 0.8


# the database memory shrink from 4G to 2G
running command `gunicorn bench.wsgi  -w 5 --threads 8 -t 360`

as you can see standard CPython is much slower than than PHP. and compare only python between python + database,the time increased ratio is as same as PHP(4.276/7.978~~2.490/4.910).  

we meet problem when benchmark mariadb and postgresql, which has CONN_MAX_AGE config in settings.py.I run this test under asgi first,but the slow pg and mariadb time made me confuse, the DB server has high load average but less CPU usage,and the tcp connection between python and DB is abnormal which count more than 300, I run uvicorn with 5 workers and 8 threads which may create 40 connections theoretically.  I changed CONN_MAX_AGE from 3600 to 0,it did reduce connections, but consume the same time.  
after I changed from uvicorn to gunicorn.the consume time become acceptable.I googled and think that asgi maybe has compatible issuse with database connection, it could not reuse connection,so every request will create new connection.

The PyPy version has huge improve compared to CPython.and it is faster than PHP. but the enviroment setup is difficult than CPython.  
In CPython I and install nearly anything from conda,but in PyPy I had to install mongoengine,django_cassandra_engine in pip,and install psycopg2cffi to instead of standard psyconpg2 package.

Mongodb lost his advantage in this comparison. maybe caused by this package was writen in python. we can get benefit by run in PyPy, that make sense.  
but I can not get benefit in running Postgresql by PyPy. I get same benchmark result.