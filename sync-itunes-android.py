import shutil, os, time, unicodedata, filecmp, urllib.parse, tqdm
from io import open

timey = time.time()
os.chdir(os.path.dirname(__file__))

# # Make Paths
dest = '/Volumes/SD Card/Music/'
playlist = 'My Playlist.m3u'
printUpdates = os.path.exists(dest)
# Enable Writing New Files
writeFiles = False
# Enable Checking If Contents of Files Have Changed (Slower)
checkContents = False

# # Copy Music Folder
def mkdir(path):
	# Excludes the last item i.e. the file
	for i in range(len(path)):
		p = dest + '/'.join(path[:i])
		if not os.path.exists(p):
			os.mkdir(p)

# Read play list, exclude blank lines and comments
with open(playlist, 'rU', encoding = 'utf-8') as file:
	playlistContents = file.read()
data = [l.strip().split('/') for l in playlistContents.split('\n') if len(l) > 0 and l[0] != '#']
fileSet = set()
# Get source folder
source = '/'.join(data[0][:-3])+'/'
for i, path in tqdm.tqdm(enumerate(data), total = len(data)):
	# Make Source and Destination Names
	s = '/'.join(path)
	# Encode is required for Python 2
	p = '/'.join(path[-3:])#.encode('utf-8')
	d = dest + p
	# Fat32 and EXFAT can't handle composed unicode characters, must be decomposed
	d = unicodedata.normalize('NFD', d) if os.path.exists('/Volumes/SD Card/') else d
	if writeFiles:
		# Keep track of files, print progress
		fileSet.add(d.lower())
		# if i % 100 == 0:
		# 	print(i, time.time() - timey)
		# Copy File
		if not os.path.exists(d) or (checkContents and not filecmp.cmp(s, d)):
			mkdir(path[-3:])
			if printUpdates:
				print(i, p)
			shutil.copy2(s, d)


print(len(fileSet), time.time() - timey)

# # Copy Playlists
# Main playlist set
playlistContents2 = unicodedata.normalize('NFC', playlistContents)
playlistSet = {l.strip() for l in playlistContents2.split('\n#')}
for filename in os.listdir('.'):
	if 'm3u' in filename:
		# Read
		with open(filename, 'rU', encoding = 'utf-8') as file:
			data = file.read()
		'''
		Contents: 
		Android VLC requires precomposed unicode
		Filter songs not in main playlist (In Android VLC, playlists cannot point to non-existent files)
		Replace source paths
		Android VLC requires url encoding
		'''
		data = unicodedata.normalize('NFC', data)
		data = '\n#'.join([l.strip() for l in data.split('\n#') if l.strip() in playlistSet])
		data = data.replace(source, '')
		data = '\n'.join([line if line and line[0] == '#' else urllib.parse.quote(line) for line in data.split('\n')])
		# Update fileSet
		fileSet.add(filename.lower())
		# Write Out
		with open(filename, 'w', encoding = 'utf-8') as output:
			output.write(data)

# # Clean Up
# Remove Deleted Songs
for folder in os.walk(dest):
	for file in folder[2]:
		path = (folder[0]+'/'+file).replace('//', '/')
		if path.lower() not in fileSet:
			try:
				print(path)
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
