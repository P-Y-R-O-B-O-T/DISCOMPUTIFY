from CYPHER_PROTOCOL.CYPHER_CLIENT.cypher_client import CYPHER_CLIENT
from CYPHER_PROTOCOL.CYPHER_CLIENT.FTP.ftp_client import FTP_CLIENT
import os
import time
import json
import traceback

#$$$$$$$$$$#

def ONLINE_SIGNAL_PROCESSOR() -> None :
    pass

def OFFLINE_SIGNAL_PROCESSOR() -> None :
    pass

def FILE_RESP_HANDLER(responce: dict) -> None :
    pass

#$$$$$$$$$$#

class CLIENT_NODE() :
    def __init__(self) :
        self.load_conf()
        self.COMPUTING_CLIENT = CYPHER_CLIENT(ip=self.CONF["MASTER_NODE"],
                                              port=self.CONF["COMPUTING_PORT"],
                                              recv_buffer=self.CONF["RECV_BUFFER"],
                                              transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                              encryption_key=self.CONF["ENCRYPTION_KEY"],
                                              decryption_key=self.CONF["DECRYPTION_KEY"],
                                              responce_handler=self.responce_processor,
                                              timeout=self.CONF["TIMEOUT"])
        self.COMPUTING_CLIENT.connect()

        self.FTP_CLIENT = FTP_CLIENT(recv_chunk_size=self.CONF["RECV_CHUNK_SIZE"],
                                     transmission_chunk_size=self.CONF["TRANSMISSION_CHUNK_SIZE"],
                                     ip=self.CONF["FTP_NODE"],
                                     port=self.CONF["FTP_PORT"],
                                     encryption_key=self.CONF["ENCRYPTION_KEY"],
                                     decryption_key=self.CONF["DECRYPTION_KEY"],
                                     offline_signal_processor=OFFLINE_SIGNAL_PROCESSOR,
                                     online_signal_processor=ONLINE_SIGNAL_PROCESSOR,
                                     file_responce_trigger=None,
                                     recv_buffer=self.CONF["RECV_BUFFER"],
                                     transmission_buffer=self.CONF["TRANSMISSION_BUFFER"])

        self.QUERY_CLIENT = CYPHER_CLIENT(ip=self.CONF["QUERY_NODE"],
                                          port=self.CONF["QUERY_PORT"],
                                          recv_buffer=self.CONF["RECV_BUFFER"],
                                          transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                          encryption_key=self.CONF["ENCRYPTION_KEY"],
                                          decryption_key=self.CONF["DECRYPTION_KEY"],
                                          responce_handler=self.query_responce_processor,
                                          timeout=self.CONF["TIMEOUT"])

    def load_conf(self) :
        conf_file = open("discomputify_conf.json", "r")
        self.CONF = json.load(conf_file)

    def responce_processor(self, responce) :
        if responce["OPERATION"] == "EXEC" :
            self.EXEC_RESP = responce["DATA"]
        elif responce["OPERATION"] == "READ_NODE_LOAD" :
            self.NODE_LOAD = responce["DATA"]
        elif responce["OPERATION"] == "READ_PROCESS_STATUS" :
            self.PROCESS_STATUS = responce["DATA"]
        elif responce["OPERATION"] == "TERMINATE" :
            self.TERMINATION_STATUS = responce["DATA"]
        elif responce["OPERATION"] == "CLEAR_DATA" :
            self.CLEAR_DATA_STATUS = responce["DATA"]
        elif responce["OPERATION"] == "GET_NO_OF_NODES" :
            self.NO_NODES = responce["DATA"]["NO_NODES"]

    def query_responce_processor(self, responce) :
        if responce["OPERATION"] == "GET_DIR_NAMES" :
            self.DIRS_TO_FETCH = responce["DATA"]["DIRECTORIES"]

    def set_responce_processor(self, responce_processor_object) :
        self.responce_processor = responce_processor

    def generate_process_id(self) :
        self.PROCESS_ID = str(int(time.time()*(10**6)))

    def get_process_id(self) :
        return self.PROCESS_ID

    def set_process_id(self, process_id) :
        self.PROCESS_ID = process_id

    def upload_files(self, path) :
        files = os.listdir(path)
        for _ in files :
            self.FTP_CLIENT.upload_file_s(os.path.join(path, _),
                                          self.PROCESS_ID)

    def download_files(self) :
        self.QUERY_CLIENT.make_request(operation="GET_DIR_NAMES",
                                       data={"PROCESS_ID": self.PROCESS_ID})
        try :
            if os.path.isdir(self.PROCESS_ID) :
                os.system("rm {0} -r".format(self.PROCESS_ID))
            for _ in self.DIRS_TO_FETCH :
                self.FTP_CLIENT.fetch_file_s(_, self.PROCESS_ID)
        except :
            traceback.print_exc()
    
    def start_computing(self) :
        self.COMPUTING_CLIENT.make_request(operation="EXEC",
                                           data={"PROCESS_ID": self.PROCESS_ID})
        return self.EXEC_RESP

    def clear_data(self) :
        self.COMPUTING_CLIENT.make_request(operation="CLEAR_DATA",
                                           data={"PROCESS_ID": self.PROCESS_ID})
        self.COMPUTING_CLIENT.make_request(operation="GET_NO_OF_NODES")
        self.FTP_CLIENT.delete_file_folder(self.PROCESS_ID)
        for _ in range(1, self.NO_NODES+1) :
            self.FTP_CLIENT.delete_file_folder("{0}_{1}_{2}".format(self.PROCESS_ID, _, self.NO_NODES))
        return self.CLEAR_DATA_STATUS

    def stop_computing(self) :
        self.COMPUTING_CLIENT.make_request(operation="TERMINATE",
                                           data={"PROCESS_ID": self.PROCESS_ID})
        return self.TERMINATION_STATUS

    def get_node_load(self) :
        self.COMPUTING_CLIENT.make_request(operation="READ_NODE_LOAD")
        return self.NODE_LOAD

    def get_process_status(self) :
        self.COMPUTING_CLIENT.make_request(operation="READ_PROCESS_STATUS",
                                           data={"PROCESS_ID": self.PROCESS_ID})
        return self.PROCESS_STATUS
