
package master

from enum import Enum
import etcd

class MasterState(enum):
    Leader = 1
    Backup = 2

class Master(object):
    def __init__(self):        
        self.parent = None 
        self.master_state_watcher = None
        self.metadata = Tree(1000)
    #借助与etcd进行选主,
    def elect_master(self):  
        self.master_state_watcher = EtcdWatcher()
        self.master_state_watcher.start()
        self.master_state_watcher.join()  

    def find(self, name):
    def add_chunkserver(self, ip):
    def del_chunkserver(self, ip):
    def lease_chunkserver(self, ip):


if __name__ == "__main__":
    try:
        #master选举, 在需要使用master/slave状态的地方
        # 通过master_state_watcher进行获取.
        eletct_master()

    except Exception:
        logger.error("Etcd watcher error: {}".format(traceback.format_exc()))