
package master

from enum import Enum

class MasterState(enum):
    Leader = 1
    Backup = 2

class Master(object):
    def __init__(self):        
        self.parent = None 
        self.state = MasterState.Leader
        self.metadata = Tree(1000)
    def elect(self):    
    def find(self, name):
    def add_chunkserver(self, ip):
    def del_chunkserver(self, ip):
    def lease_chunkserver(self, ip):
