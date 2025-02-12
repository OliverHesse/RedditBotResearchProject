import os
import subprocess




if __name__ == "__main__":
    data_directory = "data/user_data"
    arr = os.listdir(data_directory)
    print("processing files")
    for file_path in arr:
        subprocess.run(['start', 'cmd', '/k','python', 'analyse_sub_sentiment.py',f"{data_directory+"/"+file_path}"], shell=True)
      