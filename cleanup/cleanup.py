import os
from pathlib import Path
from file_entensions import extension_paths

print('Clean up your downloads folder')
folder_to_track = f'C:/Users/{os.getlogin()}/Downloads/'

def cleanup():
    log = []
    for name in os.listdir(folder_to_track):
        if os.path.isfile(folder_to_track + name):

            new_name = name
            file_type = '.' + name.lower().split(".")[-1]
            new_destination = folder_to_track + extension_paths[file_type]
          
            Path(new_destination).mkdir(parents=True, exist_ok=True)
            x = 1
            while os.path.exists(os.path.join(new_destination, new_name)):
                new_name = name[:(len(name) - len(file_type))] + f' - Copy ({x})' + file_type
                x += 1
          
            os.rename(os.path.join(folder_to_track, name), 
                      os.path.join(new_destination, new_name))
          
            log.append('{:<9}{:<70}{:<8}{:<70}'.format('Moved', new_name, 'to', new_destination))
    
    print('\n'.join(log)) if len(log) > 0 else print('No files were moved')
    print('End')

cleanup()