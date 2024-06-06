import pandas as pd
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, process_function):
        self.process_function = process_function
    
    def on_created(self,event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        process_data(filename)

def process_data(filename):
    try:
        df = pd.read_json(os.getcwd()+'/step_1/'+filename)

        normalized_df = pd.json_normalize(df['cell_type'])
        df = pd.concat([df, normalized_df], axis=1)
        df = df[['name', 'cell_response']]
        df = df[['name', 'cell_response']].groupby('name')['cell_response'].mean()
        df.to_csv(f'step_2/{os.path.splitext(os.path.basename(filename))[0]}.csv')
    except Exception as e:
        print(f"Failed to extract data from {filename} Error: {e}")

def main():
    watch_dir = os.getcwd()+'/step_1'
    event_handler = NewFileHandler(process_data)

    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()
    print(f"Now monitoring folder {watch_dir} for new files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
if __name__ == '__main__':
    main()