import shutil, os, time, unicodedata, filecmp, urllib.parse, tqdm
from io import open

timey = time.time()
os.chdir(os.path.dirname(__file__))

# # Make Paths
dest = '/Volumes/SD Card/Music/'
playlist = 'My Playlist.m3u'
printUpdates = os.path.exists(dest)
# Enable Writing New Files
writeFiles = True
# Enable Checking If Contents of Files Have Changed (Slower)
checkContents = True
# Use progress bar or print every 100 files
progressBar = False

# # Copy Music Folder
# Read play list, exclude blank lines and comments
with open(playlist, encoding = 'utf-8') as file:
    playlistContents = file.read()
data = [l.strip().split('/') for l in playlistContents.split('\n') if len(l) > 0 and l[0] != '#']
fileSet = set()

class Copier:

    def __init__(self, i, path):
        self.i = i
        self.path = path

    def makePaths(self):
        # Make Source and Destination Names
        self.source = '/'.join(self.path)
        # Encode is required for Python 2
        self.short = '/'.join(self.path[-3:])#.encode('utf-8')
        self.dest = dest + self.short
        # Fat32 and EXFAT can't handle composed unicode characters, must be decomposed
        self.dest = unicodedata.normalize('NFD', self.dest) if os.path.exists('/Volumes/SD Card/') else self.dest

    def check(self):
        # Keep track of files
        fileSet.add(self.dest.lower())
        return not os.path.exists(self.dest) or (
            checkContents and
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
        if printUpdates:
            print(self.i, self.short)
        shutil.copy2(self.source, self.dest)

    def progress(self):
        # print progress
        if self.i % 100 == 0:
            print(i, time.time() - timey)

# Get source folder
source = '/'.join(data[0][:-3])+'/'
iterator = enumerate(data)
if progressBar:
    iterator = tqdm.tqdm(iterator, total = len(data))
for i, path in iterator:
    myCopier = Copier(i, path)
    myCopier.makePaths()
    if writeFiles and myCopier.check():
        myCopier.mkdir()
        myCopier.copy()
    if not progressBar:
        myCopier.progress()

print(len(fileSet), time.time() - timey)

# # Copy Playlists
# Main playlist set
playlistContents2 = unicodedata.normalize('NFC', playlistContents)
playlistSet = {l.strip() for l in playlistContents2.split('\n#')}

class Playlist:
    
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename

    def read(self):
        # Read
        with open(folder+'/'+filename, encoding = 'utf-8') as file:
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
        self.data = '\n#'.join([l.strip() for l in self.data.split('\n#') if l.strip() in playlistSet])
        self.data = self.data.replace(source, '')
        self.data = '\n'.join([line if line and line[0] == '#' else urllib.parse.quote(line) for line in self.data.split('\n')])

    def getFilename(self):
        # Make New Filename
        self.filename = f'{dest}{self.folder} {self.filename}8'
        fileSet.add(self.filename.lower())
        # Print New Playlists
        if not os.path.exists(self.filename) and printUpdates:
            print(self.filename)

    def write(self):
        # Write Out
        with open(self.filename, 'w', encoding = 'utf-8') as file:
            file.write(self.data)

for folder in ['.']:
    for filename in os.listdir(folder):
        if 'm3u' in filename:
            myPlaylist = Playlist(folder, filename)
            myPlaylist.read()
            myPlaylist.getContents()
            myPlaylist.getFilename()
            myPlaylist.write()

# # Clean Up
# Remove Deleted Songs
for folder in os.walk(dest):
    for file in folder[2]:
        path = (folder[0]+'/'+file).replace('//', '/')
        if path.lower() not in fileSet:
            try:
                print(path.lower())
                os.remove(path)
            except Exception:
                print('failed', path)

# Remove folders. Once for album, once for artist
for i in range(2):
    for folder in os.walk(dest):
        if folder[1:] == ([], []):
            os.rmdir(folder[0])
            print(folder[0])

# # Check File Count
files = [file for path in os.walk(dest) for file in path[2]]
assert len(fileSet) == len(files)
print(len(fileSet), len(files), time.time() - timey)
