import shutil, os, time, unicodedata, filecmp
from io import open

timey = time.time()
os.chdir(os.path.dirname(__file__))

# # Make Paths
dest = '/Volumes/SD Card/Music/'
playlist = 'My Playlist.m3u'
printUpdates = os.path.exists(dest)

# # Copy Music
def mkdir(path):
	# Excludes the last item i.e. the file
	for i in range(len(path)):
		p = dest + '/'.join(path[:i])
		if not os.path.exists(p):
			os.mkdir(p)

with open(playlist, 'rU', encoding = 'utf-8') as file:
	data = [l.strip().split('/') for l in file.read().split('\n') if len(l) > 0 and l[0] != '#']
fileSet = set()
source = '/'.join(data[0][:-3])+'/'
for i, path in enumerate(data):
	# Make Source and Destination Names
	s = '/'.join(path)
	# Encode is required for Python 2
	p = '/'.join(path[-3:])#.encode('utf-8')
	d = dest + p
	# Fat32 Can't handle composed unicode characters, must be decomposed
	d = unicodedata.normalize('NFD', d) if os.path.exists('/Volumes/SD Card/') else d
	# Keep track of files, print progress
	fileSet.add(d.lower())
	if i % 100 == 0:
		print(i, time.time() - timey)
	# Copy File
	if not os.path.exists(d) or not filecmp.cmp(s, d):
		mkdir(path[-3:])
		if printUpdates:
			print(i, p)
		shutil.copy2(s, d)

print(len(fileSet), time.time() - timey)

# # Copy Playlists
for filename in os.listdir('.'):
	if 'm3u' in filename:
		# Read and replace source paths
		with open(filename, 'rU', encoding = 'utf-8') as file:
			data = file.read().replace(source, '')
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
