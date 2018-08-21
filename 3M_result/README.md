# Here is a short result

Database |avg time  | 99% time | QPS    | memory usage | CPU load
-------- | -------  | -------- | ------ | ------------ | --------
redis    | 6.934ms  | 14ms     | 576.83 | 900MB        | 0.5
mongodb  | 7.416ms  | 15ms     | 539.40 | 500MB        | 0.5
mariadb  | 25.769ms | 68ms     | 155.22 | 300MB        | 2.5


database run under virtual machine with 1 CPU and 2G RAM

3M requests is the most for redis.because above that.redis will eat a half of whole memory in this suitation.and then redis bgsave will not work properly unless tweak sysctl to over_commit.

there are some error in benchmark.the problem is php uniqid generate same token cause database duplicate key error.in the next 12M benchmark,I will fix this problem.