
package master
from http.server import SimpleHTTPRequestHandler
from http.server import CGIHTTPRequestHandler
from http.server import ThreadingHTTPServer
from functools import partial
from enum import Enum
import contextlib
import sys
import os
import etcd
#from pygfs
import tree

class DualStackServer(ThreadingHTTPServer):
    def server_bind(self):
        # suppress exception when protocol is IPv4
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()

class MasterState(enum):
    Leader = 1
    Backup = 2

class MasterConfig(object):
    def __init__(self):  
        #limit of master's performance
        self.configmap = ["meta_node": 100000, "chunkserver_count", 1000]
        #current scale of master's performance
        self.statistics = ["meta_node": 0, "chunkserver_count", 0]

#for master with python, it's not lockfree to operate metadata.
class Master(object):
    def __init__(self, configmap):        
        self.parent = None 
        self.master_state_watcher = None
        #etcd to save metadata
        #metadata: the file and chunk namespaces, the mapping from files to chunks, and the locations of each chunk’s replicas. 
        #todo: refer to cfs and infinifs
        self.etcd_conn = None
        self.grpc_server = None
        #key: master node index; value: master object
        self.master_nodes = {}
        self.meta_data = Meta()
        #key: chunkserver index; value: chunksever object
        self.chunkserver_nodes = {}
        
    #start http server for healthcheck
    def start_httpserver(server_class=DualStackServer,
            handler_class=SimpleHTTPRequestHandler,
            port=8000,
            bind='127.0.0.1',
            cgi=False,
            directory=os.getcwd()):
        """Run an HTTP server on port 8000 (or the port argument).

        Args:
            server_class (_type_, optional): Class of server. Defaults to DualStackServer.
            handler_class (_type_, optional): Class of handler. Defaults to SimpleHTTPRequestHandler.
            port (int, optional): Specify alternate port. Defaults to 8000.
            bind (str, optional): Specify alternate bind address. Defaults to '127.0.0.1'.
            cgi (bool, optional): Run as CGI Server. Defaults to False.
            directory (_type_, optional): Specify alternative directory. Defaults to os.getcwd().
        """

        if cgi:
            handler_class = partial(CGIHTTPRequestHandler, directory=directory)
        else:
            handler_class = partial(SimpleHTTPRequestHandler, directory=directory)

        with server_class((bind, port), handler_class) as httpd:
            print(
                f"Serving HTTP on {bind} port {port} "
                f"(http://{bind}:{port}/) ..."
            )
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nKeyboard interrupt received, exiting.")
                sys.exit(0)


    #借助与etcd进行选主,
    def elect_master(self):  
        self.master_state_watcher = EtcdWatcher()
        self.master_state_watcher.start()
        self.master_state_watcher.join()  
    def start_grpc_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
          RouteGuideServicer(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        server.wait_for_termination()

    def find(self, name):
    def add_chunkserver(self, ip):
    def del_chunkserver(self, ip):
    def lease_chunkserver(self, ip):


if __name__ == "__main__":
    try:
        #master选举, 在需要使用master/slave状态的地方
        # 通过master_state_watcher进行获取.
        master_config = MasterConfig()
        master = Master()
        # 启动http server for healthcheck
        master.start_httpserver()
        # master选主
        master.eletct_master()

    except Exception:
        logger.error("Etcd watcher error: {}".format(traceback.format_exc()))