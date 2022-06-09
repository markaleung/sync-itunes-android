import os, filecmp, time

class Copier:

    def __init__(self, destFolder, config):
        self.fileSet = set()
        self.destFolder = destFolder
        self.config = config

    def start(self, i, path):
        self.i = i
        self.path = path        

    def makePaths(self):
        # Make Source and Destination Names
        self.source = '/'.join(self.path)
        # Encode is required for Python 2
        self.short = '/'.join(self.path[-3:])#.encode('utf-8')
        self.dest = self.destFolder + self.short
        # Fat32 and EXFAT can't handle composed unicode characters, must be decomposed
        self.dest = unicodedata.normalize('NFD', self.dest) if os.path.exists('/Volumes/SD Card/') else self.dest

    def check(self):
        # Keep track of files
        self.fileSet.add(self.dest.lower())
        return not os.path.exists(self.dest) or (
            self.config['checkContents'] and
            not filecmp.cmp(self.source, self.dest)
        )

    def mkdir(self):
        # Excludes the last item i.e. the file
        path = self.path[-3:]
        for i in range(len(path)):
            p = dest + '/'.join(path[:i])
            if not os.path.exists(p):
                os.mkdir(p)

    def copy(self):
        # Copy File
        if self.config['printUpdates']:
            print(self.i, self.short)
        shutil.copy2(self.source, self.dest)

    def progress(self):
        # print progress
        if self.i % 100 == 0:
            print(self.i, time.time() - self.config['timey'])
