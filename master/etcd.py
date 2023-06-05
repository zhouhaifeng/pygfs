

import sys
import etcd
import traceback
from log import get_logger

#参考: https://github.com/tony-yin/etcd_watcher/tree/master/etcd_watcher
#应该有更简单的办法

logger = get_logger(__name__, '/var/log/etcd_watcher.log')


class EtcdClient(object):
    def __init__(self):
        self.hostname = get_hostname()
        self.connect()
        self.ttl = 60
        self.store_dir = '/etcd_watcher'
        self.master_file = '{}/{}'.format(self.store_dir, 'master')
        self.master_value = self.hostname
        # node status
        self.Master = 'Master'
        self.Slave = 'Slave'
        self.ToMaster = 'ToMaster'
        self.ToSlave = 'ToSlave'
        self.InitMaster = 'InitMaster'
        self.InitSlave = 'InitSlave'
        # basic status: master or slave
        self.last_basic_status = None
        self.current_basic_status = None

    def connect(self):
        try:
            self.client = etcd.Client(
                host='localhost',
                port=2379,
                allow_reconnect=True,
                protocol='https',
                cert=(
                    '/etc/ssl/etcd/ssl/node-{}.pem'.format(self.hostname),
                    '/etc/ssl/etcd/ssl/node-{}-key.pem'.format(self.hostname)
                ),
                ca_cert='/etc/ssl/etcd/ssl/ca.pem'
            )
        except Exception as e:
            logger.error("connect etcd failed: {}".format(str(e)))

    def get(self, key):
        try:
            value = self.client.read(key).value
            return value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Get key {} value failed: {}".format(key, str(e)))

    def set(self, key, value):
        try:
            self.client.write(key, value)
            return value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Get key {} value failed: {}".format(key, str(e)))

    def delete(self, key):
        try:
            self.client.delete(key)
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(key))
        except Exception as e:
            logger.error("Delete key {} failed: {}".format(key, str(e)))

    def get_dir_items(self, dir_name):
        items = {}
        try:
            r = self.client.read(dir_name, recursive=True, sorted=True)
            for child in r.children:
                items[child.key] = child.value
        except Exception as e:
            logger.error("get dir items failed: {}".format(str(e)))
        return items

    def get_watcher_items(self):
        items = {}
        try:
            items = self.get_dir_items(self.store_dir)
        except Exception as e:
            logger.error("get etcd watcher items failed: {}".format(str(e)))
        return items

    def get_watcher_keys(self):
        keys = []
        try:
            items = self.get_watcher_items()
            keys = items.keys()
        except Exception as e:
            logger.error("get etcd watcher keys failed: {}".format(str(e)))
        return keys

    def create_master(self):
        logger.info('Create master.')
        try:
            self.client.write(
                self.master_file,
                self.master_value,
                ttl=self.ttl,
                prevExist=False
            )
        except Exception as e:
            logger.error("Create master failed: {}".format(str(e)))

    def get_master(self):
        try:
            master_value = self.get(self.master_file)
            return master_value
        except etcd.EtcdKeyNotFound:
            logger.error("Key {} not found.".format(self.master_file))
        except Exception as e:
            logger.error("Get master value failed: {}".format(str(e)))

    def update_master(self):
        try:
            self.client.write(
                self.master_file,
                self.master_value,
                ttl=self.ttl,
                prevValue=self.master_value,
                prevExist=True
            )
        except Exception as e:
            logger.error("Update master failed: {}".format(str(e)))


    def get_node_basic_status(self):
        node_basic_status = None
        try:
            master_value = self.get_master()
            if master_value == self.master_value:
                node_basic_status = self.Master
            else:
                node_basic_status = self.Slave
        except Exception as e:
            logger.error("get node basic status failed: {}".format(str(e)))
        return node_basic_status


def get_hostname():
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    return 


logger = get_logger(__name__, '/var/log/etcd_watcher.log')


class EtcdWatcher(Thread):
    def __init__(self, *args, **kwargs):
        self.interval = 30
        self.etcd_client = EtcdClient()
        # node status
        self.Master = 'Master'
        self.Slave = 'Slave'
        self.ToMaster = 'ToMaster'
        self.ToSlave = 'ToSlave'
        self.InitMaster = 'InitMaster'
        self.InitSlave = 'InitSlave'
        # basic status: master or slave
        self.last_basic_status = None
        self.current_basic_status = None
        super(EtcdWatcher, self).__init__(*args, **kwargs)


    def get_node_status(self):
        self.last_basic_status = self.current_basic_status
        self.current_basic_status = self.etcd_client.get_node_basic_status()
        node_status = None
        if self.current_basic_status == self.Master:
            if self.last_basic_status is None:
                node_status = self.InitMaster
            elif self.last_basic_status == self.Master:
                node_status = self.Master
            elif self.last_basic_status == self.Slave:
                node_status = self.ToMaster
            else:
                logger.error("Invalid last basic status for master: {}".format(
                    self.last_basic_status)
                )
        elif self.current_basic_status == self.Slave:
            if self.last_basic_status is None:
                node_status = self.InitSlave
            elif self.last_basic_status == self.Master:
                node_status = self.ToSlave
            elif self.last_basic_status == self.Slave:
                node_status = self.Slave
            else:
                logger.error("Invalid last basic status for slave: {}".format(
                    self.last_basic_status)
                )
        else:
            logger.error("Invalid current basic status: {}".format(
                self.current_basic_status)
            )

        return node_status

    def do_ToMaster_work(self):
        logger.info("===== do ToMaster work =====")
        pass

    def do_InitMaster_work(self):
        logger.info("===== do InitMaster work =====")
        pass

    def do_ToSlave_work(self):
        logger.info("===== do ToSlave work =====")
        pass

    def do_InitSlave_work(self):
        logger.info("===== do ToInit work =====")
        pass

    def run(self):
        try:
            logger.info("===== Init Etcd Wathcer =====")
            self.etcd_client.create_master()
            while True:
                node_status = self.get_node_status()
                logger.info("node status : {}".format(node_status))
                if node_status == self.etcd_client.ToMaster:
                    self.do_ToMaster_work()
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.InitMaster:
                    self.do_InitMaster_work()
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.Master:
                    self.etcd_client.update_master()
                elif node_status == self.etcd_client.ToSlave:
                    self.do_ToSlave_work()
                    self.etcd_client.create_master()
                elif node_status == self.etcd_client.InitSlave:
                    self.do_InitSlave_work()
                    self.etcd_client.create_master()
                elif node_status == self.etcd_client.Slave:
                    self.etcd_client.create_master()
                else:
                    logger.error("Invalid node status: {}".format(node_status))
                time.sleep(self.interval)
                self.etcd_client = EtcdClient()
        except Exception:
            logger.error("Etcd watcher run error:{}".format(traceback.format_exc()))


def get_hostname():
    with open('/etc/hostname', 'r') as f:
        hostname = f.read().strip()
    return hostname


def do_shell(cmd):
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    while p.poll() is None:
        try:
            proc = psutil.Process(p.pid)
            for c in proc.children(recursive=True):
                c.kill()
                proc.kill()
        except psutil.NoSuchProcess:
            pass
    if p.returncode == 1:
        logger.error("Cmd {} returncode is error!".format(cmd))
    return output

