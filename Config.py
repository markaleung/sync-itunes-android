import os

class Config:
    def __init__(self):
        self._set_variables()
        self._set_updates()
    def _set_variables(self):
        self.write_files = True
        self.check_contents = True
        self.playlist_folders = ['.']
        self.dest = '/Volumes/SD Card/Music/'
        self.playlist = 'My Playlist.m3u'
    def _set_updates(self):
        self.print_updates = os.path.exists(self.dest)