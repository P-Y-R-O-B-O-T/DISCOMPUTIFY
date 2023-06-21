from CYPHER_PROTOCOL.CYPHER_SERVER.FTP.ftp_server import FTP_SERVER
from CYPHER_PROTOCOL.CYPHER_SERVER.cypher_server import CYPHER_SERVER
import time
import os
import traceback
import json

#$$$$$$$$$$#

class FTP_NODE() :
    def __init__(self) :
        self.load_conf()
        self.FTP_SERVER_OBJ = FTP_SERVER(path=self.CONF["FTP_BASE_PATH"],
                                         recv_chunk_size=self.CONF["RECV_CHUNK_SIZE"],
                                         transmission_chunk_size=self.CONF["TRANSMISSION_CHUNK_SIZE"],
                                         host=self.CONF["FTP_NODE"],
                                         port=self.CONF["FTP_PORT"],
                                         encryption_key=self.CONF["ENCRYPTION_KEY"],
                                         decryption_key=self.CONF["DECRYPTION_KEY"],
                                         recv_buffer=self.CONF["RECV_BUFFER"],
                                         transmission_buffer=self.CONF["TRANSMISSION_BUFFER"],
                                         timeout=self.CONF["TIMEOUT"],
                                         debug1=self.CONF["DEBUG1"],
                                         debug2=self.CONF["DEBUG2"])

        self.QUERY_SERVER_OBJ = CYPHER_SERVER(host=self.CONF["QUERY_NODE"],
                                              port=self.CONF["QUERY_PORT"],
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

    def handle_request(self, request, ip_port) :
        if request["OPERATION"] == "GET_FILE_NAMES" :
            try :
                dirs = os.listdir(os.path.join(self.CONF["FTP_BASE_PATH"], str(request["DATA"]["PROCESS_ID"])))
                while self.CONF["INPUT_PATH"] in dirs :
                    dirs.remove(self.CONF["INPUT_PATH"])
                while self.CONF["OUTPUT_PATH"] in dirs :
                    dirs.remove(self.CONF["OUTPUT_PATH"])
                request["DATA"]["FILES"] = dirs
            except Exception as E :
                traceback.print_exc()

        if request["OPERATION"] == "GET_DIR_NAMES" :
            dirs = os.listdir(self.CONF["FTP_BASE_PATH"])
            required_dirs = []
            for _ in dirs :
                if (request["DATA"]["PROCESS_ID"]+"_") in _ :
                    required_dirs.append(_)
            request["DATA"]["DIRECTORIES"] = required_dirs
        return request

    def start_node(self) :
        self.FTP_SERVER_OBJ.start_server()
        self.QUERY_SERVER_OBJ.start_server()

    def stop_node(self) :
        self.FTP_SERVER_OBJ.stop_server()
        self.QUERY_SERVER_OBJ.stop_server()
