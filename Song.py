import os, filecmp, shutil, unicodedata

class Copier:

    def __init__(self, config: dict):
        self.config = config
        self.fileSet = set()
    def makePaths(self):
        # Make Source and Destination Names
        self.source = '/'.join(self.path)
        # Encode is required for Python 2
        self.short = '/'.join(self.path[-3:])#.encode('utf-8')
        self.dest = self.config.dest + self.short
        # Fat32 and EXFAT can't handle composed unicode characters, must be decomposed
        self.dest = unicodedata.normalize('NFD', self.dest) if os.path.exists('/Volumes/SD Card/') else self.dest
        # Keep track of files, even when not writing
        self.fileSet.add(self.dest.lower())
    def check(self):
        return not os.path.exists(self.dest) or (
            self.config.check_contents and
            # File contents have changed
            not filecmp.cmp(self.source, self.dest)
        )
    def mkdir(self):
        # Excludes the last item i.e. the file
        if self.config.write_files:
            path = self.path[-3:]
            for i in range(len(path)):
                p = self.config.dest + '/'.join(path[:i])
                if not os.path.exists(p):
                    os.mkdir(p)
    def copy(self):
        # Copy File
        if self.config.print_updates:
            print(self.i, self.short)
        if self.config.write_files:
            shutil.copy2(self.source, self.dest)
    def main(self, i, path):
        self.i = i
        self.path = path        
        self.makePaths()
        if self.check():
            self.mkdir()
            self.copy()
