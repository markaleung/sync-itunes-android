import unicodedata, urllib.parse, os

class Copier:
    def __init__(self, config, playlistSet: set):
        self.config = config
        self.playlistSet = playlistSet
        self.fileSet = set()
    def read(self):
        # Read
        with open(self.folder+'/'+self.filename, encoding = 'utf-8') as file:
            self.data = file.read()
    def getContents(self):
        '''
        Contents: 
        Android VLC requires precomposed unicode
        Filter songs not in main playlist (In Android VLC, playlists cannot point to non-existent files)
        Replace source paths
        Android VLC requires url encoding
        '''
        self.data = unicodedata.normalize('NFC', self.data)
        self.data = '\n#'.join([l.strip() for l in self.data.split('\n#') if l.strip() in self.playlistSet])
        self.data = self.data.replace(self.config.source, '')
        self.data = '\n'.join([line if line and line[0] == '#' else urllib.parse.quote(line) for line in self.data.split('\n')])
    def getFilename(self):
        # Make New Filename
        self.filename = f'{self.config.dest}{self.folder} {self.filename}8'
        self.fileSet.add(self.filename.lower())
        # Print New Playlists
        if not os.path.exists(self.filename) and self.config.print_updates:
            print(self.filename)
    def write(self):
        # Write Out
        with open(self.filename, 'w', encoding = 'utf-8') as file:
            file.write(self.data)
    def main(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.read()
        self.getContents()
        self.getFilename()
        self.write()

class Manager:
    def __init__(self, config):
        self.config = config
    def preCopyPlaylists(self):
        # Get source folder for Playlist
        self.config.source = '/'.join(self.config.fileList[0][:-3])+'/'
        # Playlist set for copying playlists
        playlistMain = unicodedata.normalize('NFC', self.config.playlistMain)
        self.playlistSet = {l.strip() for l in playlistMain.split('\n#')}
        # Start Playlist
        self.playlistCopier = Copier(self.config, self.playlistSet)
    def copyPlaylists(self):
        for folder in self.config.playlist_folders:
            for filename in os.listdir(folder):
                if 'm3u' in filename:
                    self.playlistCopier.main(folder, filename)
    def main(self):
        self.preCopyPlaylists()
        self.copyPlaylists()
        
