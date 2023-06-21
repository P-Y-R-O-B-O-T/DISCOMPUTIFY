import sys

def run_node() :
    if "computing_node" in sys.argv :
        from .COMPUTING_NODE.computing_node import COMPUTING_NODE
        try :
            COMPUTING_NODE_OBJ = COMPUTING_NODE()
            COMPUTING_NODE_OBJ.start_node()
            input()
            COMPUTING_NODE_OBJ.stop_node()
        except Exception as E :
            print(E)
            exit(0)
    if "master_node" in sys.argv :
        from .MASTER_NODE.master_node import MASTER_NODE
        try :
            MASTER_NODE_OBJ = MASTER_NODE()
            MASTER_NODE_OBJ.start_node()
            input()
            MASTER_NODE_OBJ.stop_node()
        except Exception as E :
            print(E)
            exit(0)
    if "ftp_node" in sys.argv :
        from .FTP_NODE.ftp_node import FTP_NODE
        try :
            FTP_NODE_OBJ = FTP_NODE()
            FTP_NODE_OBJ.start_node()
            input()
            FTP_NODE_OBJ.stop_node()
        except Exception as E :
            print(E)
            exit(0)

run_node()
