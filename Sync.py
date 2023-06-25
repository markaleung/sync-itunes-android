import os, unicodedata, tqdm

import Song, Playlist

class Sync:

    def __init__(self, config: dict):
        self.config = config
        self.fileSet = set()

    def readPlaylist(self):
        with open(self.config['playlist'], encoding = 'utf-8') as file:
            self.playlistMain = file.read()

    # Songs
    def preCopySongs(self):
        # File list for copying songs, exclude blank lines and comments
        self.fileList = [l.strip().split('/') for l in self.playlistMain.split('\n') if len(l) > 0 and l[0] != '#']
        # Enumerate and add progress bar
        self.iterator = tqdm.tqdm(enumerate(self.fileList), total = len(self.fileList))
        # Start Songs
        self.songCopier = Song.Copier(self.config)        

    def copySongs(self):
        for i, path in self.iterator:
            self.songCopier.start(i, path)
            self.songCopier.makePaths()
            if self.config['writeFiles'] and self.songCopier.check():
                self.songCopier.mkdir()
                self.songCopier.copy()
        self.fileSet |= self.songCopier.fileSet

    # Playlists
    def preCopyPlaylists(self):
        # Get source folder for Playlist
        self.config['source'] = '/'.join(self.fileList[0][:-3])+'/'
        # Playlist set for copying playlists
        playlistMain = unicodedata.normalize('NFC', self.playlistMain)
        self.playlistSet = {l.strip() for l in playlistMain.split('\n#')}
        # Start Playlist
        self.playlistCopier = Playlist.Copier(self.config, self.playlistSet)

    def copyPlaylists(self):
        for folder in self.config['playlistFolders']:
            for filename in os.listdir(folder):
                if 'm3u' in filename:
                    self.playlistCopier.start(folder, filename)
                    self.playlistCopier.read()
                    self.playlistCopier.getContents()
                    self.playlistCopier.getFilename()
                    self.playlistCopier.write()
        self.fileSet |= self.playlistCopier.fileSet

    # Clean Up
    def cleanSong(self, path: str):
        if path.lower() not in self.fileSet:
            print(path.lower())
            if self.config['writeFiles']:
                os.remove(path)

    def cleanSongs(self):
        for folder in os.walk(self.config['dest']):
            for file in folder[2]:
                path = (folder[0]+'/'+file).replace('//', '/')
                self.cleanSong(path)

    def cleanFolder(self, folder: tuple):
        if folder[1:] == ([], []):
            if self.config['writeFiles']:
                os.rmdir(folder[0])
            print(folder[0])

    def cleanFolders(self):
        for i in range(2):
            for folder in os.walk(self.config['dest']):
                self.cleanFolder(folder)

    # Check Files
    def checkFiles(self):
        files = [file for path in os.walk(self.config['dest']) for file in path[2]]
        assert len(self.fileSet) == len(files)
        print(len(self.fileSet), len(files))

    def main(self):
        self.readPlaylist()
        # Songs
        self.preCopySongs()
        self.copySongs()
        # Playlists
        self.preCopyPlaylists()
        self.copyPlaylists()
        # Clean Up
        self.cleanSongs()    
        self.cleanFolders()
        # Check
        self.checkFiles()