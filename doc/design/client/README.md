gfs api与posix api不兼容(append), 因此不需要基于libfuse开发client
对于面向容器使用的CFS,需兼容posix file api,便于应用使用

bigtable中保存网址,路径,文件名, bigtable解决跨dc, 单dc单gfs cluster规模不足以保存整个互联网所有网页
因为在bigtable中可以看到所有文件, gfs client不必兼容主机文件系统,在前端主机上不必看到写入的文件, client的应用方为网页爬虫等程序

主机上保存log
client支持以cli/lib两种模式访问gfs
client与master交互,创建文件, master返回主副本所在chunkindex, 