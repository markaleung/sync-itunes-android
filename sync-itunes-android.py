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

class Copier:

	def makePaths(self, i, path):
		self.i = i
		self.path = path
		# Make Source and Destination Names
		self.s = '/'.join(path)
		# Encode is required for Python 2
		self.p = '/'.join(path[-3:])#.encode('utf-8')
		self.d = dest + self.p
		# Fat32 and EXFAT can't handle composed unicode characters, must be decomposed
		self.d = unicodedata.normalize('NFD', self.d) if os.path.exists('/Volumes/SD Card/') else self.d

	def copy(self):
		# Keep track of files, print progress
		fileSet.add(self.d.lower())
		# if i % 100 == 0:
		# 	print(i, time.time() - timey)
		# Copy File
		if not os.path.exists(self.d) or (checkContents and not filecmp.cmp(self.s, self.d)):
			mkdir(self.path[-3:])
			if printUpdates:
				print(self.i, self.p)
			shutil.copy2(self.s, self.d)

# Get source folder
source = '/'.join(data[0][:-3])+'/'
for i, path in tqdm.tqdm(enumerate(data), total = len(data)):
	myCopier = Copier()
	myCopier.makePaths(i, path)
	if writeFiles:
		myCopier.copy()

print(len(fileSet), time.time() - timey)

# # Copy Playlists
# Main playlist set
playlistContents2 = unicodedata.normalize('NFC', playlistContents)
playlistSet = {l.strip() for l in playlistContents2.split('\n#')}

class Playlist:

	def read(self, folder, filename):
		self.folder = folder
		self.filename = filename
		# Read
		with open(folder+'/'+filename, 'rU', encoding = 'utf-8') as file:
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

	def write(self):
		# Print New Playlists
		if not os.path.exists(self.filename) and printUpdates:
			print(self.filename)
		# Write Out
		with open(self.filename, 'w', encoding = 'utf-8') as output:
			output.write(self.data)

for folder in ['.']:
	for filename in os.listdir(folder):
		if 'm3u' in filename:
			myPlaylist = Playlist()
			myPlaylist.read(folder, filename)
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
