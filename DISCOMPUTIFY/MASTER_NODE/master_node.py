from CYPHER_PROTOCOL.CYPHER_SERVER.cypher_server import CYPHER_SERVER
from CYPHER_PROTOCOL.CYPHER_CLIENT.cypher_client import CYPHER_CLIENT
import threading
import psutil
import time
import multiprocessing
import threading
import json
import traceback

NODE_STATUS = True

#$$$$$$$$$$#

class COMPUTING_NODES() :
    def __init__(self) :
        self.LOCK = threading.Lock()
        self.TERMINATED_PROCESSES = {}
        self.STARTED_PROCESSES = {}
        self.PROCESS_STATUS = {}
        self.NODE_LOAD = {}
        self.LOAD = {}

        self.load_conf()
        self.get_valid_ip_addresses()
        self.create_client_objects()
        self.start_internal_processes()

    def load_conf(self) :
        conf_file = open("discomputify_conf.json", "r")
        self.CONF = json.load(conf_file)

    def get_valid_ip_addresses(self) :
        for _ in range(len(self.CONF["COMPUTING_NODES"])) :
            if "\n" in self.CONF["COMPUTING_NODES"][_] :
                self.CONF["COMPUTING_NODES"][_] = self.CONF["COMPUTING_NODES"][_][:-1]

        valid_ip_addresses = []

        for _ in self.CONF["COMPUTING_NODES"] :
            if self.validate_ip(_) :
                valid_ip_addresses.append(_)
        self.IP_ADDRESSES = valid_ip_addresses

    def create_client_objects(self) :
        clients = []
        file_clients = []
        status_clients = []
        for _ in self.IP_ADDRESSES :
            clients.append(CYPHER_CLIENT(ip=_,
                                         port=self.CONF["COMPUTING_PORT"],
                                         recv_buffer=self.CONF["RECV_BUFFER"],
                                         transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                         encryption_key=self.CONF["ENCRYPTION_KEY"],
                                         decryption_key=self.CONF["DECRYPTION_KEY"],
                                         responce_handler=self.responce_processor,
                                         timeout=self.CONF["TIMEOUT"]))
            clients[-1].connect()
        self.CLIENTS = clients

    def start_internal_processes(self) :
        thread_fetch_node_load = threading.Thread(target=self.fetch_node_load)
        thread_fetch_node_load.start()

    def responce_processor(self, responce) :
        if responce["OPERATION"] == "READ_NODE_LOAD" :
            self.process_read_node_load_responce(responce)
        if responce["OPERATION"] == "READ_PROCESS_STATUS" :
            self.process_read_process_status_responce(responce)
        if responce["OPERATION"] == "EXEC" :
            self.process_exec_responce(responce)
        if responce["OPERATION"] == "TERMINATE" :
            self.process_termination_responce(responce)

    def process_termination_responce(self, responce) :
        if responce["DATA"]["PROCESS_ID"] not in self.TERMINATED_PROCESSES :
            self.TERMINATED_PROCESSES[responce["DATA"]["PROCESS_ID"]] = {}
        self.TERMINATED_PROCESSES[responce["DATA"]["PROCESS_ID"]][responce["DATA"]["NODE_NAME"]] = responce["DATA"]["STATUS"]

    def process_read_node_load_responce(self, responce) :
        self.NODE_LOAD[responce["DATA"]["NODE_NAME"]] = responce["DATA"]["LOAD"]

    def process_read_process_status_responce(self, responce) :
        if responce["DATA"]["PROCESS_ID"] not in self.PROCESS_STATUS :
            self.PROCESS_STATUS[responce["DATA"]["PROCESS_ID"]] = {}
        self.PROCESS_STATUS[responce["DATA"]["PROCESS_ID"]][responce["DATA"]["NODE_NAME"]] = responce["DATA"]["STATUS"]

    def process_exec_responce(self, responce) :
        if responce["DATA"]["PROCESS_ID"] not in self.STARTED_PROCESSES :
            self.STARTED_PROCESSES[responce["DATA"]["PROCESS_ID"]] = {}
        self.STARTED_PROCESSES[responce["DATA"]["PROCESS_ID"]][responce["DATA"]["NODE_NAME"]] = responce["DATA"]["PROCESS_STATUS"]

    def validate_ip(self, ip) :
        ip_split = ip.split(".")
        if len(ip_split) != 4 :
            return False
        for _ in ip_split :
            try :
                part_int = int(_)
                if not (0 <= part_int < 256) :
                    return False
            except :
                return False
        return True

    def execute_on_every_node(self, params) :
        self.LOCK.acquire()
        for _ in range(len(self.CLIENTS)) :
            self.CLIENTS[_].make_request(operation=params["OPERATION"],
                                         data={"PROCESS_ID": params["DATA"]["PROCESS_ID"],
                                               "PART": str(_+1),
                                               "TOTAL_PARTS": len(self.CLIENTS)
                                               },
                                         metadata=params["METADATA"]
                                         )
        self.LOCK.release()
        return self.STARTED_PROCESSES[params["DATA"]["PROCESS_ID"]]

    def terminate_on_every_node(self, params) :
        self.LOCK.acquire()
        for _ in range(len(self.CLIENTS)) :
            self.CLIENTS[_].make_request(operation=params["OPERATION"],
                                         data=params["DATA"],
                                         metadata=params["METADATA"]
                                         )
        self.LOCK.release()
        return self.TERMINATED_PROCESSES[params["DATA"]["PROCESS_ID"]]

    def fetch_node_load(self) :
        while NODE_STATUS :
            self.LOCK.acquire()
            for _ in self.CLIENTS :
                if NODE_STATUS :
                    _.make_request(operation="READ_NODE_LOAD")
                else :
                    pass
            self.LOCK.release()
            time.sleep(1)

    def get_node_load(self) :
        return self.NODE_LOAD

    def get_no_nodes(self) :
        return len(self.CLIENTS)

    def get_process_status(self, params) :
        self.LOCK.acquire()
        for _ in self.CLIENTS :
            if NODE_STATUS :
                _.make_request(operation="READ_PROCESS_STATUS",
                               data={"PROCESS_ID": params["DATA"]["PROCESS_ID"]},
                               metadata=params["METADATA"]
                               )
        self.LOCK.release()
        return self.PROCESS_STATUS[params["DATA"]["PROCESS_ID"]]

    def remove_started_status(self, process_id) :
        del self.STARTED_PROCESSES[process_id]

    def remove_process_status(self, process_id) :
        del self.PROCESS_STATUS[process_id]

    def remove_termination_status(self, process_id) :
        del self.TERMINATED_PROCESSES[process_id]

    def clear_data(self, process_id) :
        try : del self.STARTED_PROCESSES[process_id]
        except : pass
        try : del self.PROCESS_STATUS[process_id]
        except : pass
        try : del self.TERMINATED_PROCESSES[process_id]
        except : pass

    def stop_all_communiation(self) :
        for _ in self.CLIENTS :
            _.close_connection()

#$$$$$$$$$$#

class MASTER_NODE() :
    def __init__(self) :
        self.load_conf()
        self.COMPUTING_NODES_OBJ = COMPUTING_NODES()
        self.COMPUTING_SERVER = CYPHER_SERVER(host=self.CONF["MASTER_NODE"],
                                              port=self.CONF["COMPUTING_PORT"],
                                              recv_buffer=self.CONF["RECV_BUFFER"],
                                              transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                              encryption_key=self.CONF["ENCRYPTION_KEY"],
                                              decryption_key=self.CONF["DECRYPTION_KEY"],
                                              request_handler=self.request_processor,
                                              timeout=self.CONF["TIMEOUT"],
                                              debug1=self.CONF["DEBUG1"],
                                              debug2=self.CONF["DEBUG2"])

    def load_conf(self) :
        conf_file = open("discomputify_conf.json", "r")
        self.CONF = json.load(conf_file)

    def request_processor(self, request, ip_port) :
        try :
            if request["OPERATION"] == "READ_NODE_LOAD" :
                self.process_read_node_load(request)
            if request["OPERATION"] == "READ_PROCESS_STATUS" :
                self.process_read_process_status(request)
            if request["OPERATION"] == "TERMINATE" :
                self.process_terminate_process(request)
            if request["OPERATION"] == "EXEC" :
                self.process_exec_process(request)
            if request["OPERATION"] == "CLEAR_DATA" :
                self.process_clear_data(request)
            if request["OPERATION"] == "GET_NO_OF_NODES" :
                self.get_nodes(request)
            return request
        except :
            traceback.print_exec()

    def get_nodes(self, request) :
        request["DATA"] = {}
        request["DATA"]["NO_NODES"] = self.COMPUTING_NODES_OBJ.get_no_nodes()

    def process_read_node_load(self, request) :
        request["DATA"] = self.COMPUTING_NODES_OBJ.get_node_load()

    def process_read_process_status(self, request) :
        request["DATA"] = self.COMPUTING_NODES_OBJ.get_process_status(request)

    def process_terminate_process(self, request) :
        request["DATA"] = self.COMPUTING_NODES_OBJ.terminate_on_every_node(request)

    def process_exec_process(self, request) :
        request["DATA"] = self.COMPUTING_NODES_OBJ.execute_on_every_node(request)

    def process_clear_data(self, request) :
        self.COMPUTING_NODES_OBJ.clear_data(request["DATA"]["PROCESS_ID"])

    def start_node(self) :
        self.COMPUTING_SERVER.start_server()

    def stop_node(self) :
        global NODE_STATUS
        NODE_STATUS = False
        self.COMPUTING_SERVER.stop_server()
        self.COMPUTING_NODES_OBJ.stop_all_communiation()
