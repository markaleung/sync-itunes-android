import os, unicodedata, tqdm

import Song, Playlist

class Sync:

    def __init__(self, config):
        self.config = config
        self.fileSet = set()
    def readPlaylist(self):
        with open(self.config.playlist, encoding = 'utf-8') as file:
            self.config.playlistMain = file.read()
    def copySongs(self):
        self.songs = Song.Manager(config = self.config)
        self.songs.main()
        self.fileSet |= self.songs.songCopier.fileSet
    def copyPlaylists(self):
        self.playlists = Playlist.Manager(config = self.config)
        self.playlists.main()
        self.fileSet |= self.playlists.playlistCopier.fileSet
    # Clean Up
    def cleanSong(self, path: str):
        if path.lower() not in self.fileSet:
            print(path.lower())
            if self.config.write_files:
                os.remove(path)
    def cleanSongs(self):
        for folder in os.walk(self.config.dest):
            for file in folder[2]:
                path = (folder[0]+'/'+file).replace('//', '/')
                self.cleanSong(path)
    def cleanFolder(self, folder: tuple):
        if folder[1:] == ([], []):
            if self.config.write_files:
                os.rmdir(folder[0])
            print(folder[0])
    def cleanFolders(self):
        for i in range(2):
            for folder in os.walk(self.config.dest):
                self.cleanFolder(folder)
    # Check Files
    def checkFiles(self):
        files = [file for path in os.walk(self.config.dest) for file in path[2]]
        assert len(self.fileSet) == len(files)
        print(len(self.fileSet), len(files))
    def main(self):
        self.readPlaylist()
        # Songs
        self.copySongs()
        # Playlists
        self.copyPlaylists()
        # Clean Up
        self.cleanSongs()    
        self.cleanFolders()
        # Check
        self.checkFiles()