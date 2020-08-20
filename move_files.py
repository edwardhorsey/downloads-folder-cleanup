import os
from pathlib import Path
from file_entensions import extension_paths

def move():
    folder_to_track = 'C:\\Users\\Edward\\Downloads\\myFolderOne'
    folder_destination = 'C:\\Users\\Edward\\Downloads\\myFolderTwo'
    for name in os.listdir(folder_to_track):
        file_type = '.' + name.split(".")[-1]
        new_destination = folder_destination + '/' + extension_paths[file_type]
        Path(new_destination).mkdir(parents=True, exist_ok=True)  
        os.rename(os.path.join(folder_to_track, name), 
                  os.path.join(new_destination, name))

move()