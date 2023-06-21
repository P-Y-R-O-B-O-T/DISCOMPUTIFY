from DISCOMPUTIFY.BASE_PROGRAM.base_program import *
import time

#$$$$$$$$$$#
#python3 <program_name> <i th part> <n parts> <FILE_INPUT_PATH> <FILE_OUTPUT_PATH> <FTP_HOST>
#$$$$$$$$$$#

"""
class FileNotFound(Exception) :
    def __init__(self,
                 file_name) :
        super().__init__("File {0} not found !!"
                         .format(file_name))

#$$$$$$$$$$#

class CanNotGoUpInDirectory(Exception) :
    def __init__(self,
                 file_name) :
        super().__init__("File name can not have .. at any place ({0}),\n"
                         .format(file_name)+
                         "can not go any level up in directory hierarchy")

#$$$$$$$$$$#

class FileNotFoundAtInputPath(Exception) :
    def __init__(self,
                 file_name) :
        super().__init__("File {0} not found in input path !!"
                         .format(file_name))

#$$$$$$$$$$#

class CanNotOpenFileAtOutputPath(Exception) :
    def __init__(self,
                 file_name) :
        super().__init__("File {0} not found in input path !!"
                         .format(file_name))

#$$$$$$$$$$#

class UtilityClassNotInitialized(Exception) :
    def __init__(self) :
        super().__init__("First initialize the utility class and set params,"+
                         "then get assess the utilities")

#$$$$$$$$$$#

class UTILITY() :
    CONF = None

    @classmethod
    def initialized(self) :
        if self.CONF != None :
            return True
        return False

    @classmethod
    def set_params(self,
                   params) :
        self.load_conf()

        self.PART = int(params[1])
        self.TOTAL_PARTS = int(params[2])
        self.PROGRAM_NAME_PROCESS_ID = params[3]

        print("$$$$$$$$$", self.PART, self.TOTAL_PARTS, self.PROGRAM_NAME_PROCESS_ID)

        #self.FTP_CLIENT_OBJ = FTP_CLIENT()

        self.FTP_CLIENT_OBJ = FTP_CLIENT(recv_chunk_size=self.CONF["RECV_CHUNK_SIZE"],
                                         transmission_chunk_size=self.CONF["TRANSMISSION_CHUNK_SIZE"],
                                         ip=self.CONF["FTP_NODE"],
                                         port=self.CONF["FTP_PORT"],
                                         encryption_key=self.CONF["ENCRYPTION_KEY"],
                                         decryption_key=self.CONF["DECRYPTION_KEY"],
                                         file_responce_trigger=None,
                                         recv_buffer=self.CONF["RECV_BUFFER"],
                                         transmission_buffer=self.CONF["TRANSMISSION_BUFFER"])

        os.chdir(self.PROGRAM_NAME_PROCESS_ID)

    @classmethod
    def load_conf(self) :
        conf_file = open("discomputify_conf.json", "r")
        self.CONF = json.load(conf_file)

    @classmethod
    def part(self) :
        if self.initialized() :
            return self.PART
        raise UtilityClassNotInitialized()

    @classmethod
    def total_parts(self) :
        if self.initialized() :
            return self.TOTAL_PARTS
        raise UtilityClassNotInitialized()

    @classmethod
    def open_file(self,
                  path,
                  mode) :
        if self.initialized() :
            if ".." not in path :
                if "r" in mode :
                    try :
                        if not os.path.isfile(os.path.join(self.CONF["INPUT_PATH"],
                                                           path)) :
                            self.FTP_CLIENT_OBJ.fetch_file_s(os.path.join(self.PROGRAM_NAME_PROCESS_ID,
                                                                          self.CONF["INPUT_PATH"],
                                                                          path),
                                                             self.CONF["INPUT_PATH"])
                        return open(os.path.join(self.CONF["INPUT_PATH"],
                                                 path),
                                    mode)
                    except Exception as E :
                        raise FileNotFoundAtInputPath(path)
                if "a" in mode or "w" in mode :
                    if not os.path.isdir(self.CONF["OUTPUT_PATH"]) :
                        os.mkdir(self.CONF["OUTPUT_PATH"])
                    try :
                        return open(os.path.join(self.CONF["OUTPUT_PATH"],
                                                 path),
                                    mode)
                    except Exception as E :
                        raise CanNotOpenFileAtOutputPath(path)
            else :
                raise CanNotGoUpInDirectory(path)
        raise UtilityClassNotInitialized()

    def read_from_output(self,
                         path) :
        if self.initialized() :
            if ".." not in path :
                try :
                    return open(os.path.join(self.CONF["OUTPUT_PATH"],
                                             path),
                                "r")
                except :
                    CanNotOpenFileAtOutputPath(path)
            else :
                raise CanNotGoUpInDirectory(path)
        raise UtilityClassNotInitialized()

"""

#$$$$$$$$$$#

def qwe() :
    for _ in range(10) :
        time.sleep(1)
        print("PRPGRAM PROGRAM PROGRAM")

#qwe()

UTILITY.load_conf()
print(sys.argv)
UTILITY.set_params(sys.argv)
f = UTILITY.open_file("RANDOM.txt", "w")
f.write("QWEQEWQE")
f.close()
time.sleep(10)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! OPENING FILE")
f = UTILITY.open_file("init.vim", "r")
a = f.read()
print(a)
f.close()
