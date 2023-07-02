google gfs开源实现
gfs v1:
https://pdos.csail.mit.edu/6.824/papers/gfs.pdf
gfs v2:
https://www.sohu.com/a/413895492_673711

共5个组件, client, master, chunkserver, etcd, rocksdb 
client支持cli, api, rpc, chunkserver
master支持rpc, 主备, 元数据, 租约, chunkserver管理
chunkserver支持rpc, 缓存, 租约, log, 一致性, io调度, 副本, gc, ec, 文件管理

特性列表:
支持通过client open/close/write/read file(一个client为一个进程)
支持master保存metadata
支持chunkserver管理
支持io管理
支持chunk操作日志
支持chunk创建/read/write/snapshot
支持副本

规格:
client: 1000
master: 3
chunkserver: 1000
file: 100M

限制: 
不兼容posix api
不支持fuse
不支持nfs