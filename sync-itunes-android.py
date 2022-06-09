import os, time, unicodedata, tqdm
import Copier, Playlist
from io import open

os.chdir(os.path.dirname(__file__))

# # Make Paths
config = {
    # Enable Writing New Files
    'writeFiles': True, 
    # Enable Checking If Contents of Files Have Changed (Slower)
    'checkContents': True, 
    # Use progress bar or print every 100 files
    'progressBar': False, 
    'timey': time.time(), 
	'dest': '/Volumes/SD Card/Music/', 
	'playlist': 'My Playlist.m3u', 
}
config['printUpdates'] = os.path.exists(config['dest'])

# # Copy Music Folder
# Read play list, exclude blank lines and comments
with open(config['playlist'], encoding = 'utf-8') as file:
    playlistContents = file.read()
data = [l.strip().split('/') for l in playlistContents.split('\n') if len(l) > 0 and l[0] != '#']

# Get source folder
config['source'] = '/'.join(data[0][:-3])+'/'
iterator = enumerate(data)
if config['progressBar']:
    iterator = tqdm.tqdm(iterator, total = len(data))
# Copy each file
myCopier = Copier.Copier(config)
for i, path in iterator:
    myCopier.start(i, path)
    myCopier.makePaths()
    if config['writeFiles'] and myCopier.check():
        myCopier.mkdir()
        myCopier.copy()
    if not config['progressBar']:
        myCopier.progress()

print(len(myCopier.fileSet), time.time() - config['timey'])

# # Copy Playlists
# Main playlist set
playlistContents2 = unicodedata.normalize('NFC', playlistContents)
playlistSet = {l.strip() for l in playlistContents2.split('\n#')}

# Copy each playlist
myPlaylist = Playlist.Playlist(config, playlistSet)
for folder in ['.']:
    for filename in os.listdir(folder):
        if 'm3u' in filename:
            myPlaylist.start(folder, filename)
            myPlaylist.read()
            myPlaylist.getContents()
            myPlaylist.getFilename()
            myPlaylist.write()

fileSet = myCopier.fileSet | myPlaylist.fileSet

# # Clean Up
# Remove Deleted Songs
for folder in os.walk(config['dest']):
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
    for folder in os.walk(config['dest']):
        if folder[1:] == ([], []):
            os.rmdir(folder[0])
            print(folder[0])

# # Check File Count
files = [file for path in os.walk(config['dest']) for file in path[2]]
assert len(fileSet) == len(files)
print(len(fileSet), len(files), time.time() - config['timey'])
