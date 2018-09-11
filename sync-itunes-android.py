import fileinput, shutil, os, time

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

fileSet = set()
data = [l.strip().split('/') for l in fileinput.input(playlist) if l[0] != '#']
source = '/'.join(data[0][:-3]) + '/'
timey = time.time()
for i, path in enumerate(data):
	# Make Source and Destination Names
	s = '/'.join(path)
	d = dest+'/'.join(path[-3:])
	# Other Stuff
	fileSet.add(d.lower())
	if i % 500 == 0:
		print(i, time.time() - timey)
	# Copy File
	mkdir(path[-3:])
	if not os.path.exists(d):
		if printUpdates:
			print(d)
		shutil.copy2(s, d)

print(len(fileSet), time.time() - timey)

# # Copy Playlists
for filename in os.listdir('.'):
	if 'm3u' in filename:
		# Read and replace source paths
		with open(filename) as file:
			data = file.read().replace(source, '')
		fileSet.add(filename.lower())
		# Write Out
		with open(filename, 'w') as output:
			output.write(data)

# # Clean Up
# Remove Deleted Songs
for folder in os.walk(dest):
	for file in folder[2]:
		path = (folder[0]+'/'+file).replace('//', '/')
		if path.lower() not in fileSet:
			try:
				os.remove(path)
				print(path)
			except Exception:
				pass

# Once for album, once for artist
for i in range(2):
	for folder in os.walk(dest):
		if folder[1:] == ([], []):
			os.rmdir(folder[0])
			print(folder[0])

# # Check
files = [file for path in os.walk(dest) for file in path[2]]
print(len(fileSet), len(files))
