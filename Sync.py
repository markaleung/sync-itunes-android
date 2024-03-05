import os, unicodedata, tqdm

import Song, Playlist, Cleaner

class Sync:

    def __init__(self, config):
        self.config = config
    def readPlaylist(self):
        with open(self.config.playlist, encoding = 'utf-8') as file:
            self.config.playlistMain = file.read()
    def copySongs(self):
        self.songs = Song.Manager(config = self.config)
        self.songs.main()
    def copyPlaylists(self):
        self.playlists = Playlist.Manager(config = self.config)
        self.playlists.main()
    # Clean Up
    def cleanSongs(self):
        self.song_cleaner = Cleaner.Song(config = self.config)
        self.song_cleaner.main()
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
        assert len(self.config.file_set) == len(files)
        print(len(self.config.file_set), len(files))
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