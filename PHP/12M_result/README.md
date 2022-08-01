# Here is a short result

Database |avg time  | 99% time | QPS    | disk usage   | memory usage|  CPU load
-------- | -------  | -------- | ------ | ------------ | ----------  | ---------
php only | 2.490ms  | 6ms      | 1606.22 | N/A         | N/A         | N/A
php json | 2.710ms  | 6ms      | 1476.04 | N/A         | N/A         | N/A
mongodb  | 4.910ms  | 9ms      | 814.61 | 0.7G         | 509MB       | 1.2
redis    | 5.882ms  | 12ms     | 679.98 | 0.6G         | 1421MB      | 0.7
mariadb  | 6.163ms  | 12ms     | 648.99 | 3.1G         | 2081MB      | 2.0
cassandra| 6.287ms  | 18ms     | 636.22 | 1.0G         | 1551MB      | 1.0
postgresql| 6.381ms | 11ms     | 626.89 | 3.2G         | 1048MB      | 1.2

The result shows whichever database you use.In session(token) suition.It only take 3ms(another 3ms consume by php and lumen framework) to do that.

the winner is mongodb,not only wined by the least time consume,also winned by disk, memory usage and CPU load.and I guess mongodb use data compress so it's disk usage is so small and no need json encode also reduce the total time.

While benchmark meet a lumen problem. lumen init mysql connection takes too long about 10ms.I haven't figure that out.so I wrote pure mariadb pdo code to do the benchmark.

the postgresql also has some advantages compare to traditional relation database. that use less memory and CPU. I can't find a way to store jsonb through php, if that work then maybe has better disk usage.

the redis has little advantages on the CPU load item, because it use single core. so it keep the same result while using half compute resources.

I think the total loser is mariadb in this scenario.

## TODO
bench all database in Python.