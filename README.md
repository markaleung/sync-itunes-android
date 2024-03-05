# sync-itunes-android
- This script makes it easy to sync an itunes playlist to an SD Card so that you can play your music on an Android phone. 
- The reason that you need an SD card is because I couldn't figure out how to use the terminal to access an Android phone that is plugged in to your computer. 
- This script assumes that you have told iTunes to organise your library for you, so that the file paths are consistent (/path/to/itunes music/artist/album/song.mp3). 
- I have only tested this script on a Mac. I'm not sure whether you might have bugs when running it on Windows. 

# How to Use this Script
- Use iTunes to export each of your playlists to an m3u file. 
- Download this script to the same folders as your playlists. 
- Change 'dest' to the location of the folder in the SD Card where you want to store all the music and playlist files. 
	- If the folder exists already, the script will print every new file that is copied to the folder. I did this because I assumed that if the folder existed, the script had already run once, so the script would print any files that have been added to the playlist since the last time you ran it. 
- Change 'playlist' to the name of the playlist that contains all of the songs you want to sync. 
	- All other playlist files will be copied to the folder so that you can use them in your music player, but only the specified playlist file is used to determine which songs will be synced. 
- Run the script using `notebook_itunes.ipynb`. 

# Function Tree
- Sync.readPlaylist()
	- open()
- Sync.copySongs()
	- Song.Manager.preCopySongs
	- Song.Manager.copySongs
		- for i, path in iterator:
			- Song.Copier.makePaths()
			- Song.Copier.check()
			- Song.Copier.mkdir()
			- Song.Copier.copy()
- Sync.copyPlaylists()
	- Playlist.Manager.preCopyPlaylists
	- Playlist.Manager.copyPlaylists
		- for folder in config['playlistFolders']:
			- for filename in os.listdir(folder):
				- Playlist.Copier.read()
				- Playlist.Copier.getContents()
				- Playlist.Copier.getFilename()
				- Playlist.Copier.write()
- Sync.cleanSongs()
	- for folder in os.walk(self.config.dest):
		- for file in folder[2]:
			- Cleaner.Song.cleanSong
- Sync.cleanFolders()
	- for i in range(2):
		- for self.folder in os.walk(self.config.dest):
			- Cleaner.Folder.cleanFolder
- Sync.checkFiles()