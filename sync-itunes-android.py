import os, time, unicodedata, tqdm
import Song, Playlist
from io import open

os.chdir(os.path.dirname(__file__))

config = {
    # Enable Writing New Files
    'writeFiles': True, 
    # Enable Checking If Contents of Files Have Changed (Slower)
    'checkContents': True, 
    # Use progress bar or print every 100 files
    'progressBar': True, 
    'timey': time.time()
}
if os.path.exists('/Volumes/SD Card/'):
    config.update({
        'dest': '/Volumes/SD Card/Music/', 
        'playlist': 'Workflow/Shuffle Source.m3u', 
    })
else:
    config.update({
        'dest': '/Users/mark/Desktop/Music/', 
        'playlist': 'Workflow/A Scratch 2.m3u', 
    })
    config['printUpdates'] = os.path.exists(config['dest'])

class Sync:

    def __init__(self):
        self.config = config
        self.fileSet = set()

    def readPlaylist(self):
        # Read play list, exclude blank lines and comments
        with open(self.config['playlist'], encoding = 'utf-8') as file:
            self.playlistMain = file.read()

    def preCopySongs(self):
        # File list for copying songs
        self.fileList = [l.strip().split('/') for l in self.playlistMain.split('\n') if len(l) > 0 and l[0] != '#']
        # Enumerate and add progress bar
        self.iterator = enumerate(self.fileList)
        if self.config['progressBar']:
            self.iterator = tqdm.tqdm(self.iterator, total = len(self.fileList))
        # Start copier
        self.songCopier = Song.Copier(self.config)        

    def copySongs(self):
        for i, path in self.iterator:
            self.songCopier.start(i, path)
            self.songCopier.makePaths()
            if self.config['writeFiles'] and self.songCopier.check():
                self.songCopier.mkdir()
                self.songCopier.copy()
            if not self.config['progressBar']:
                self.songCopier.progress()
        self.fileSet |= self.songCopier.fileSet
        print(len(self.fileSet), time.time() - self.config['timey'])

    def preCopyPlaylists(self):
        # Get source folder for Playlist
        self.config['source'] = '/'.join(self.fileList[0][:-3])+'/'
        # Playlist set for copying playlists
        playlistMain = unicodedata.normalize('NFC', self.playlistMain)
        self.playlistSet = {l.strip() for l in playlistMain.split('\n#')}
        # Start Playlist
        self.playlistCopier = Playlist.Copier(self.config, self.playlistSet)

    def copyPlaylists(self):
        for folder in 'Collections Favourites Setlists Workflow'.split(' '):
            for filename in os.listdir(folder):
                if 'm3u' in filename:
                    self.playlistCopier.start(folder, filename)
                    self.playlistCopier.read()
                    self.playlistCopier.getContents()
                    self.playlistCopier.getFilename()
                    self.playlistCopier.write()
        self.fileSet |= self.playlistCopier.fileSet

    def cleanSongs(self):
        for folder in os.walk(self.config['dest']):
            for file in folder[2]:
                path = (folder[0]+'/'+file).replace('//', '/')
                if path.lower() not in self.fileSet:
                    try:
                        print(path.lower())
                        os.remove(path)
                    except Exception:
                        print('failed', path)

    def cleanFolders(self):
        for i in range(2):
            for folder in os.walk(self.config['dest']):
                if folder[1:] == ([], []):
                    os.rmdir(folder[0])
                    print(folder[0])

    def checkFiles(self):
        files = [file for path in os.walk(self.config['dest']) for file in path[2]]
        assert len(self.fileSet) == len(files)
        print(len(self.fileSet), len(files), time.time() - self.config['timey'])

if __name__=='__main__':
    mySync = Sync()
    mySync.readPlaylist()
    
    mySync.preCopySongs()
    mySync.copySongs()
    
    mySync.preCopyPlaylists()
    mySync.copyPlaylists()
    
    mySync.cleanSongs()    
    mySync.cleanFolders()
    
    mySync.checkFiles()
