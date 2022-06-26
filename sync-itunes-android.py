import os, time, unicodedata, tqdm
import Sync
from io import open

os.chdir(os.path.dirname(__file__))

config = {
    # Enable Writing New Files
    'writeFiles': True, 
    # Enable Checking If Contents of Files Have Changed (Slower)
    'checkContents': True, 
    # File locations
    'playlistFolders': ['.'], 
    'dest': '/Volumes/SD Card/Music/', 
    'playlist': 'My Playlist.m3u', 
}
# Print updates on subsequent tries. On first try, there will be too many updates
config['printUpdates'] = os.path.exists(config['dest'])

Sync.Sync(config).main()
