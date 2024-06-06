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
        folder = os.getcwd()+'/step_2'
        process_data(folder)

def process_data(folder):
    num_of_correct_hyptoesis_experiments = 0
    num_of_experiments = 0
    try:
        for file in os.listdir(folder):
            if file.endswith('.csv'):
                num_of_experiments+=1
                file_path = os.path.join(folder,file)
                c_df = pd.read_csv(file_path)
                if c_df.loc[c_df['cell_response'].idxmax(),'name'] == 'Neuron':
                    num_of_correct_hyptoesis_experiments+=1
    except Exception as e:
        print(f"Error processing file {file}. Error: {e}")
    
    hyp_correction_val = (num_of_correct_hyptoesis_experiments/num_of_experiments)*100
    
    print(f'hypothesis is true for: {hyp_correction_val}%')
        

def main():
    watch_dir = os.getcwd()+'/step_2'
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