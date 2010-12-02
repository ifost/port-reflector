"""This module defines Tee, a file-like object which you can 
write to. But you construct it by giving it several files as
arguments. When you write to the Tee, it writes it to the files
underneath."""

class Tee:
    def __init__(self,*filelist):
        self.__outfiles = {}
        for f in filelist:
            if type(f) == type({}):
                for elem in f.keys():
                    self.__outfiles[elem] = f[elem]
            elif type(f)==file:
                self.__outfiles[f] = ""
            else:
                raise ValueError,f
        self.mode = 'w'
    def write(self,s):
        for f in self.__outfiles.keys():
            f.write(self.__outfiles[f]+s)
    def close(self):
        for f in self.__outfiles.keys():
            f.close()
    def flush(self):
        for f in self.__outfiles.keys():
            f.flush()
    def writelines(self,sequence_of_strings):
        for s in sequence_of_strings:
            self.write(s)
