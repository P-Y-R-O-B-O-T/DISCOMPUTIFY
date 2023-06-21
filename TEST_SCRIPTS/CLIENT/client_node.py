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
