from CYPHER_PROTOCOL.CYPHER_SERVER.cypher_server import CYPHER_SERVER
from CYPHER_PROTOCOL.CYPHER_CLIENT.cypher_client import CYPHER_CLIENT
from CYPHER_PROTOCOL.CYPHER_CLIENT.FTP.ftp_client import FTP_CLIENT
import threading
import psutil
import time
import multiprocessing
import os
import json
import traceback

NODE_STATUS = True

#$$$$$$$$$$#

class SYS_LOAD() :
    def __init__(self) :
        self.CPU_LOAD = 0
        self.MEM_LOAD = 0
        self.MEM_USED = 0
        self.LOAD_CPU_THREAD = threading.Thread(target=self.get_cpu_load)
        self.LOAD_MEM_THREAD = threading.Thread(target=self.get_mem_load)

        self.LOAD_CPU_THREAD.start()
        self.LOAD_MEM_THREAD.start()

    def get_cpu_load(self) :
        while NODE_STATUS :
            self.CPU_LOAD = psutil.cpu_percent(2)
            time.sleep(1)

    def get_mem_load(self) :
        while NODE_STATUS :
            mem_usage = psutil.virtual_memory()
            total_mem = mem_usage[0]/(10**9) # converting to GB
            self.MEM_LOAD = mem_usage[2]
            self.MEM_USED = total_mem*(self.MEM_LOAD/100)
            time.sleep(1)

    def get_load(self) :
        return {"CPU_LOAD": self.CPU_LOAD,
                "MEM_LOAD": self.MEM_LOAD,
                "MEM_USED": self.MEM_USED}

#$$$$$$$$$$#

class COMPUTING_NODE() :
    def __init__(self) :
        self.load_conf()
        self.PROCESSES = {}
        self.FILES = {}
        self.SERVER_OBJ = CYPHER_SERVER(host=self.CONF["COMP_NODE"],
                                        port=self.CONF["COMPUTING_PORT"],
                                        recv_buffer=self.CONF["RECV_BUFFER"],
                                        transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                        encryption_key=self.CONF["ENCRYPTION_KEY"],
                                        decryption_key=self.CONF["DECRYPTION_KEY"],
                                        request_handler=self.handle_request,
                                        timeout=self.CONF["TIMEOUT"],
                                        debug1=self.CONF["DEBUG1"],
                                        debug2=self.CONF["DEBUG2"])

    def load_conf(self) :
        conf_file = open("discomputify_conf.json", "r")
        self.CONF = json.load(conf_file)

    def initiate_process(self,
                         params) :
        try :
            self.PROCESSES[params["DATA"]["PROCESS_ID"]] = multiprocessing.Process(target=self.process,
                                                                                   args=(params,))
            self.PROCESSES[params["DATA"]["PROCESS_ID"]].start()
        except Exception as E :
            print(E)

    def process(self,
                params) :
        query_client = CYPHER_CLIENT(ip=self.CONF["QUERY_NODE"],
                                     port=self.CONF["QUERY_PORT"],
                                     encryption_key=self.CONF["ENCRYPTION_KEY"],
                                     decryption_key=self.CONF["DECRYPTION_KEY"],
                                     responce_handler=self.handle_query_request,
                                     recv_buffer=self.CONF["RECV_BUFFER"],
                                     transmission_buffer=self.CONF["TRANSMISSION_BUFFER"])
        query_client.make_request(operation="GET_FILE_NAMES",
                                  data={"PROCESS_ID": params["DATA"]["PROCESS_ID"]})
        files = self.FILES[params["DATA"]["PROCESS_ID"]]
        query_client.close_connection()
        del query_client
        ftp_client = FTP_CLIENT(file_responce_trigger=None,
                                recv_chunk_size=self.CONF["RECV_CHUNK_SIZE"],
                                transmission_chunk_size=self.CONF["TRANSMISSION_CHUNK_SIZE"],
                                ip=self.CONF["FTP_NODE"], port=self.CONF["FTP_PORT"],
                                encryption_key=self.CONF["ENCRYPTION_KEY"],
                                decryption_key=self.CONF["DECRYPTION_KEY"],
                                recv_buffer=self.CONF["RECV_BUFFER"],
                                transmission_buffer=self.CONF["TRANSMISSION_BUFFER"])
        for _ in files :
            ftp_client.fetch_file_s("{0}/{1}".format(params["DATA"]["PROCESS_ID"], _), params["DATA"]["PROCESS_ID"])
        file_path = "{0}/{1}".format(params["DATA"]["PROCESS_ID"], "main.py")
        os.system("python3 {0} {1} {2} {3}".format(file_path,
                                                   params["DATA"]["PART"],
                                                   params["DATA"]["TOTAL_PARTS"],
                                                   params["DATA"]["PROCESS_ID"]
                                                   ))

        ftp_client.upload_file_s("{0}/{1}".format(params["DATA"]["PROCESS_ID"], self.CONF["OUTPUT_PATH"]),
                                 "{0}_{1}_{2}".format(params["DATA"]["PROCESS_ID"],
                                                      params["DATA"]["PART"],
                                                      params["DATA"]["TOTAL_PARTS"]))

    def handle_query_request(self,
                             responce) :
        if responce["OPERATION"] == "GET_FILE_NAMES" :
            self.FILES[responce["DATA"]["PROCESS_ID"]] = responce["DATA"]["FILES"]

    def handle_request(self,
                       request: dict,
                       ip_port: tuple) -> None :
        try :
            if request["OPERATION"] == "READ_NODE_LOAD" :
                self.read_load(request)
            if request["OPERATION"] == "READ_PROCESS_STATUS" :
                self.read_process_status(request)
            if request["OPERATION"] == "EXEC" :
                self.create_process(request)
            if request["OPERATION"] == "TERMINATE" :
                self.terminate_process(request)
            return request
        except Exception as E :
            traceback.print_exc()

    def create_process(self,
                       request) :
        request["DATA"]["NODE_NAME"] = self.CONF["COMP_NODE"]
        if request["DATA"]["PROCESS_ID"] not in self.PROCESSES :
            self.initiate_process(request)
            request["DATA"]["PROCESS_STATUS"] = "STARTED"
        else :
            if not self.PROCESSES[request["DATA"]["PROCESS_ID"]].is_alive() :
                self.initiate_process(request)
                request["DATA"]["PROCESS_STATUS"] = "STARTED"
            else :
                request["DATA"]["PROCESS_STATUS"] = "ALREADY_RUNNING"

    def read_load(self,
                  request) :
        request["DATA"] = {"NODE_NAME": self.CONF["COMP_NODE"],
                           "LOAD": SYS_LOAD_OBJ.get_load()}

    def read_process_status(self,
                            request) :
        try :
            request["DATA"]["NODE_NAME"] = self.CONF["COMP_NODE"]
            try :
                request["DATA"]["STATUS"] = self.PROCESSES[request["DATA"]["PROCESS_ID"]].is_alive()
            except :
                request["DATA"]["STATUS"] = False
        except Exception as E:
            print(E)
            request["DATA"]["NODE_NAME"] = self.CONF["COMP_NODE"]
            request["DATA"]["STATUS"] = False

    def terminate_process(self,
                          request) :
        request["DATA"]["NODE_NAME"] = self.CONF["COMP_NODE"]
        if request["DATA"]["PROCESS_ID"] in self.PROCESSES :
            try :
                self.PROCESSES[request["DATA"]["PROCESS_ID"]].terminate()
            except : pass
            finally :
                try :
                    del self.PROCESSES[request["DATA"]["PROCESS_ID"]]
                except : pass
            request["DATA"]["STATUS"] = "TERMINATED"
        else :
            request["DATA"]["STATUS"] = "DO_NOT_EXIST"

    def start_node(self) :
        self.SERVER_OBJ.start_server()

    def stop_node(self) :
        global NODE_STATUS
        self.SERVER_OBJ.stop_server()
        NODE_STATUS = False

#$$$$$$$$$$#

SYS_LOAD_OBJ = SYS_LOAD()
