# Benchmark for Session Database
In my past experience,session database must be fast enough,because every request need to access session database.

so the first in mind is memory key-value database like redis.everyone would think like me.

but with the growth of UV ,more session will created.and redis will eat more memory.5G,10G,20G eg.the result is we can't affort that much memory,it's too expensive.It's nearly cost than our main mysql server.

I have to figure it out.I want to find a database is as fast as redis.and will store data into disk not all in memory.so after a little research I found someone.

- ~~rocksdb (too bad.only for embedded)~~
- ~~ardb (backend with rocksdb.but still need lots of memory)~~
- mongodb v4.0 (seems wiredtiger engine is awesome)
- ~~cassandra (too bad.there is no driver for php 7.2)~~
- mariadb v10.3 (some times database for )
- redis v4.0 (for baseline)

# Environment

- My Old laptop thinkpad W520 which CPU is i7-2860QM(4C8T)
- ab command run on host.php and database run on seperate virtualbox machine
- all virtual machine are ubuntu 18.04
- all virtual machine run on an old SATA SSD
- php is 7.2 and redis use phpredis not predis for faster speed
- php framwork is lumen 5.6.
- other software config are all default.

# What actions I test

In the benchmark.I test three actions.

* Insert new session
* find the inserted session
* update that session timestmap

# Result

The result is in 3M_result folder.which means that is a 3,000,000 requests result.

same as 12M_result.I test for 12M result because that will over eat redis memory,I want to know so much dataset will or will not different to the 3M dataset

And The winner is All.Yes! All of three databases.there is no big different each other.but redis is still the fastest if you care about performance under 1ms.

