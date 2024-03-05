import os
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
    def cleanSongs(self):
        self.song_cleaner = Cleaner.Song(config = self.config)
        self.song_cleaner.main()
    def cleanFolders(self):
        self.folder_cleaner = Cleaner.Folder(config = self.config)
        self.folder_cleaner.main()
    def checkFiles(self):
        files = [file for path in os.walk(self.config.dest) for file in path[2]]
        assert len(self.config.file_set) == len(files)
        print(len(self.config.file_set), len(files))
    def main(self):
        self.readPlaylist()
        self.copySongs()
        self.copyPlaylists()
        self.cleanSongs()    
        self.cleanFolders()
        self.checkFiles()