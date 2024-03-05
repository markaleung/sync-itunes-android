import os

class Song:
    def __init__(self, config):
        self.config = config
    def cleanSong(self):
        if self.path.lower() not in self.config.file_set:
            print(self.path.lower())
            if self.config.write_files:
                os.remove(self.path)
    def main(self):
        for folder in os.walk(self.config.dest):
            for file in folder[2]:
                self.path = (folder[0]+'/'+file).replace('//', '/')
                self.cleanSong()

class Folder:
    def __init__(self, config):
        self.config = config
    def cleanFolder(self):
        if self.folder[1:] == ([], []):
            if self.config.write_files:
                os.rmdir(self.folder[0])
            print(self.folder[0])
    def main(self):
        for i in range(2):
            for self.folder in os.walk(self.config.dest):
                self.cleanFolder()
