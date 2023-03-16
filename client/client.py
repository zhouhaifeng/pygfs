
package client

import sys



class Client(object):
    def __init__(self):
        self.meta = {}

    def create(self, ns, filename, mode):
    def delete(self, ns, filename):
    def open(self, ns, fd):
    def close(self, ns, fd):
    def read(self, ns, chunkindex, fd, buffer, offset):
    def write(self, ns, chunkindex, fd, buffer, offset):
    def append(self, ns, chunkindex, fd, buffer):

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
