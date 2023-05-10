
package client

import sys



class Client(object):
    def __init__(self):
        self.meta = {}
    #posix:
    #int open(const char *pathname,int flags,int perms)
    #int close(int fd)
    #ssize_t&nbsp;read(int fd, void *buf, size_t count);
    #ssize_t write(int fd, void *buf, size_t count);
    #off_t lseek(int fd, off_t offset,int whence)
    #
    def open(self, ns, flags, perms):
    def close(self, fd):
    def read(self, fd, chunkindex, count):
    def write(self, fd, chunkindex, buf, count):
    #ntroduced an atomic append operation so that multiple clients can append concurrently to a file 
    # without extra synchronization between them
    def append(self, fd, chunkindex, ns, flags, perms, buf):

'''client.py {put|get} filename'''
if __name__ == '__main__': 
    client = Client()
    if client == None:
        return

    '''client.py put filename'''
    op = sys.argv[1]
    if op == "put":
        if sys.argv[2] == ""
            print("no filename!\r\n")
            return

        client.write(sys.argv[2])
    elseif op == "get":
        if sys.argv[2] == ""
            print("no filename!\r\n")
            return
        client.read(sys.argv[2])

    return
