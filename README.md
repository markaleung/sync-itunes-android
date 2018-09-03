# sync-itunes-android
- This script makes it easy to sync an itunes playlist to an SD Card so that you can play your music on an Android phone. 
- The reason that you need an SD card is because it's difficult to use the terminal to access an Android phone that is plugged in to your computer. 

# How to Use this Script
- Use iTunes to export each of your playlists to an m3u file. 
- Download this script to the same folders as your playlists. 
- Change 'dest' to the location of the folder in the SD Card where you want to store all the music and playlist files. 
  - If the folder exists already, the script will print every new file that is copied to the folder. I did this because I assumed that if the folder existed, the script had already run once, so the script would print any files that have been added to the playlist since the last time you ran it. 
- Change 'playlist' to the name of the playlist that contains all of the songs you want to sync. 
  - All other playlist files will be copied to the folder so that you can use them in your music player, but only the specified playlist file is used to determine which songs will be synced. 
- Run the script using the terminal. 