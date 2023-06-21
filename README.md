# DISCOMPUTIFY

![](ZZZ/ZZZ.jpg)

* [PROJECT LINK GITHUB](https://github.com/P-Y-R-O-B-O-T/DISCOMPUTIFY)
* [PROJECT LINK PYPI](https://pypi.org/project/discomputify-P-Y-R-O-B-O-T/)

* A library written purely in python to do distributed computing using CYPHER-PROTOCOL.

* Many times the task is very large and only single thread or single computer is not sufficient to do the computation, specially when the tasks are independent of each other or partially depend on each other.

* Thus we need to run the programs in parallel maner to complete the computation process faster and effeciently.

# COMPATIBLITY

* READPY works with Linux, OS-X, and Windows (OS INDEPENDENT).

* Supported on python 3.10 and above

# INSTALLATION

> Install it using pip.

* Goto [PYPI](https://pypi.org/project/discomputify-P-Y-R-O-B-O-T/)

# USAGE

## CONFIGURATION
* For configuration of server and client need a configuration file named discomputify_conf.json

### CONFIG PARAMETERS
* `RECV_BUFFER` and `TRANSMISSION_BUFFER` are parameters both should have same corresponding value for both server and client configuration.

* `ENCRYPTION_KEY` and `DECRYPTION_KEY` are parameters which ensure encryption of data sent over connection, see CYPHER-PROTOCOL documentation for more information.

* `TIMEOUT` is the time after which a connection is closed or reset from client side or server side.

* `RECV_CHUNK_SIZE` and `TRANSMISSION_CHUNK_SIZE` are the parameters that control chunk size for file transfers

* `DEBUG1` and `DEBUG2` control the debug levels of CYPHER_PROTOCOL

* `INPUT_PATH` and `OUTPUT_PATH` are parameters that specify the relative path for storing and retrieving  input and output files

* `FTP_NODE`, `QUERY_NODE`, `MASTER_NODE`, `SHARED_MEM_NODE` specify the addresses where the particiler service nodes are running

* `FTP_PORT`, `QUERY_PORT`, `MASTER_PORT`, `SHARED_MEM_PORT` specify the ports at which these particular services are running or will be running

* `FTP_BASE_PATH` is to set the base path of files in FTP so that there is no clash between namespaces and files are perfectly organised

* `COMPUTING_NODES` is an array of addresses of computing services available

* `COMP_NODE` is used to set address of computing node while starting a computing service

* Example discomputify_conf is given in CONF_FILES folder, consider that for more details.

## STARTING A COMPUTING SERVICE
* Put discomputify_conf.json in a directory and run the command
```bash
python3 -m DISCOMPUTIFY computing_node
```

## STARTING A FTP SERVICE
* Put discomputify_conf.json in a directory and run the command
```bash
python3 -m DISCOMPUTIFY ftp_node
```

## STARTING A MASTER NODE SERVICE
* Put discomputify_conf.json in a directory and run the command
```bash
python3 -m DISCOMPUTIFY master_node
```

## USAGE OF CLIENT FOR DISTRIBUTED COMPUTING
* For starting computation, create a directory and put all the input files for the program in a directory as specified in discompitify_conf.json

* then add the program that you want to run with all of its dependencies in the directory, but make sure that the starting poin of your program should be main.py

* See an example of main.py in test_scripts

* Here is the example for using the CLIENT_NODE for computing

```python
from DISCOMPUTIFY.CLIENT_NODE.client_node import CLIENT_NODE
import time

if __name__ == "__main__" :
    CLIENT_NODE_OBJ = CLIENT_NODE()
    CLIENT_NODE_OBJ.set_process_id("1684340918413322")

    print("UPLOADING FILES")
    CLIENT_NODE_OBJ.upload_files("qwe")
    print("UPLOADING COMPLETE")

    print("STARTING COMPUTING")
    print(CLIENT_NODE_OBJ.start_computing())
    print("COMPUTING STARTED")

    time.sleep(1)
    
    print("GETTING NODE LOAD")
    print(CLIENT_NODE_OBJ.get_node_load())
    print("GETTING PROCESS STATUS")
    
    print(CLIENT_NODE_OBJ.get_process_status())
    
    #print("TERMINATING PROCESS")
    #CLIENT_NODE_OBJ.stop_computing()
    #print("PROCESS TERMINATED")

    print("GETTING PROCESS STATUS")
    print(CLIENT_NODE_OBJ.get_process_status())
    print("GOT PROCESS STATUS")

    print("GETTING FILES")
    CLIENT_NODE_OBJ.download_files()
    print("DOWNLOADED FILES")

    #print("CLEARING DATA")
    #print(CLIENT_NODE_OBJ.clear_data())
    #print("CLEARED DATA")
```
