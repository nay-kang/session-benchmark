# Benchmark for Session Database
In my past experience,session database must be fast enough,because every request need to access the session database.

so the first in mind is memory key-value database like redis.like anyone else.

but with the growth of UV ,more session will be generated.and redis will eat more memory.5G,10G,20G eg.the result is we can't affort that much memory,it's too expensive.It's nearly cost more than our main mysql server.

I have to figure it out.I want to find a database which as fast as redis.and will store data into disk rather in memory.so after a little research I found someone.

- ~~rocksdb (too bad.only for embedded)~~
- ~~ardb (backend with rocksdb.but still need lots of memory)~~
- mongodb v6.0 (seems wiredtiger engine is awesome)
- cassandra v4.0 (lack of support for php,I had to compile the ext by myself)
- mariadb v10.3 (some times database for )
- redis v5.0 (for baseline)

# Environment

- My laptop lenovo legion which CPU is R5800H(8C16T)
- ab command run on host.php and database run on seperate qemu machine
- all virtual machine are ubuntu 20.04
- all virtual machine run on an nvme SSD
- php is 7.4 and redis use phpredis not predis for faster speed
- php framwork is lumen 8.0.
- php run in 4 CPUs and 2G ram, database run in 2 CPUs and 4G ram.
- mariadb server do some basic tweak.
- other software config are all default.

# What actions I test

In the benchmark.I test three actions.

* Insert new session
* find the inserted session
* update that session timestmap

# Result

The result is in 12M_result folder.which means that is a 12,000,000 requests result.

## Quick Answer
The winner is Mongodb.I had this new answer after 4 years re-benchmark

in this special scenario the mongodb is the fastest,least memory and disk usage.we will talk about the result in the 12M_result folder.

