import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from file_entensions import extension_paths

class Watcher:
    def __init__(self):
        self.observer = Observer()
        self.log = self.start_log()
        self.folder_to_track = f'C:/Users/{os.getlogin()}/Downloads/'

    def start_log(self):
        begin = time.strftime(f"%d/%m/%Y %H:%M:%S", time.localtime())
        return ["Log:", f"Start: {begin}"]

    def end_log(self):
        end = time.strftime(f"%d/%m/%Y %H:%M:%S", time.localtime())
        self.log.append(f"Finish: {end}")

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.folder_to_track, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Stopping... \n")
            if len(self.log) < 3:
                self.log.append('No files were moved')
            self.end_log()
            print('\n'.join(self.log))
            print('End')
        self.observer.join()

    def cleanup(self, file_path):
        if os.path.isfile(file_path):

            name = file_path.split("/")[-1]
            file_type = '.' + name.lower().split(".")[-1]
            new_destination = self.folder_to_track + extension_paths[file_type]
            new_name = name

            Path(new_destination).mkdir(parents=True, exist_ok=True)
            x = 1
            while os.path.exists(os.path.join(new_destination, new_name)):
                new_name = name[:(len(name) - len(file_type))] + f' - Copy ({x})' + file_type
                x += 1

            os.rename(os.path.join(self.folder_to_track, name), 
                      os.path.join(new_destination, new_name))

            self.log.append('{:<9}{:<60}{:<9}{:<60}'.format('Moved', new_name, 'to', new_destination))
            print(f'Moved {name}')

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            watcher.cleanup(event.src_path)
        elif event.event_type == 'modified':
            watcher.cleanup(event.src_path)

if __name__ == '__main__':
    watcher = Watcher()
    print('Clean up your downloads folder')
    print('Press Ctrl-C to stop watching')
    watcher.run()