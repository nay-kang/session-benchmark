# Here is a short result

Database |avg time  | 99% time | QPS    | disk usage | CPU load
-------- | -------  | -------- | ------ | ------------ | --------
mongodb  | 7.503ms  | 16ms     | 533.14 | 0.9G         | N/A
mariadb  | 7.538ms  | 15ms     | 530.67 | 3.2G         | 2.5


database still run under virtual machine with 1 CPU and 2G RAM

As 3M requests is the most for redis.so this 12M requests round benchmark redis will not present.

While benchmark mariadb meet lots of problems.

* lumen init mysql connection takes too long about 10ms.I haven't figure that out.so I wrote pure mariadb pdo code to do the benchmark.
* eat whole disk space.because mariadb default enable binlog.thus mongodb not enable cluster mode.so I disable binlog
* eat whole memory.so I have to adjust some buffer parameter to mariadb.


The result shows whichever database you use.In session(token) suition.It only take 2ms(5ms consume by lumen framework) to do that.and I guess mongodb use data compress so it's disk usage is so small.