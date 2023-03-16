google gfs开源实现
https://pdos.csail.mit.edu/6.824/papers/gfs.pdf

共4个组件, client, master, chunkserver, etcd
client支持cli, api, rpc, chunkserver
master支持rpc, 主备, 元数据, rocksdb, chunkserver管理
chunkserver支持rpc, 缓存, io调度, 副本, ec, 文件管理