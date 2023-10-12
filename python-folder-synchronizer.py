import os 
import shutil
import logging
import hashlib # Library for comparison of file content by md5 hash
import sys
import time

# Logging to file
logging.basicConfig(filename='synchronizer-actions.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

passedArguments = sys.argv

def verify_arguments(passed_arguments):
   expected_number_of_arguments = 3
   # Removed first argument, because it is name of the file
   cleansed_arguments = passed_arguments[1:]
   if len(cleansed_arguments) == expected_number_of_arguments:
      interval, source_folder_path, replica_folder_path = cleansed_arguments
      try:
         interval = int(interval)
         validate_path(source_folder_path)
         validate_path(replica_folder_path)
         return interval, source_folder_path, replica_folder_path
      except ValueError as ve:
        print(f"Error: {ve}")
      except Exception as e:
        print(f"Unexpected error: {e}")   
   else:
      print("Invalid number of values passed! Check number of paramaters and run application again.")

def validate_path(path):
       if not os.path.exists(path):
        raise ValueError(f"Path: {path} does not exist.")
       if not os.path.isdir(path):
        raise ValueError(f"Path: {path} is not a directory.")
       
def copy_source_entry(source_entry_path, source_folder_path, replica_folder_path):
  try:
    destinationPath = create_destination_path(source_entry_path, source_folder_path, replica_folder_path)
    if os.path.isfile(source_entry_path):
      shutil.copy2(source_entry_path, destinationPath)
    elif os.path.isdir(source_entry_path):
      shutil.copytree(source_entry_path, destinationPath)
    logging.info(f"Copied: {source_entry_path} to {destinationPath}")
    print(f"Copied: {source_entry_path} to {destinationPath}")
  except Exception as e: 
        logging.error(f"Error copying {source_entry_path} to {destinationPath}: {str(e)}")
        print(f"Error: {str(e)}")

def delete_destination_entry(destination_entry_path):
  try:
    if os.path.isfile(destination_entry_path):
      os.remove(destination_entry_path)
    elif os.path.isdir(destination_entry_path):
      shutil.rmtree(destination_entry_path)
    logging.info(f"Deleted: {destination_entry_path}")
    print(f"Deleted: {destination_entry_path}")
  except Exception as e: 
        logging.error(f"Error deleting {destination_entry_path}: {str(e)}")
        print(f"Error: {str(e)}")

def create_destination_path(source_path, source_folder_path, replica_folder_path):
  return source_path.replace(source_folder_path, replica_folder_path)

def create_source_path(destination_path, source_folder_path, replica_folder_path):
   return destination_path.replace(replica_folder_path, source_folder_path)

# This function verifies whether the content of a file remains consistent and is utilized to replace files if the content is not identical
def get_file_hash(file_path):
   hasher = hashlib.md5()
   with open(file_path, "rb") as file:
      buf = file.read()
      hasher.update(buf)
   return hasher.hexdigest()

def compare_file_content(entry_path, destination_entry_path):
   return get_file_hash(entry_path) != get_file_hash(destination_entry_path)

def compare_folder_content(source_folder_path, replica_folder_path):
  # Copying files and folders to replica directory, if new file or folder will appear in source directory
  for root, dirs, files in os.walk(source_folder_path):
     allEntries = dirs + files
     for entryName in allEntries:
        entryPath = os.path.join(root, entryName)
        destinationEntryPath = create_destination_path(entryPath, source_folder_path, replica_folder_path)
        # Comparing file content by hash must be second, because the file needs to exists first.
        if not os.path.exists(destinationEntryPath) or (os.path.isfile(entryPath) and compare_file_content(entryPath, destinationEntryPath)):
          logging.info(f"New entry was created on this path: {entryPath}")
          print(f"New entry was created on this path: {entryPath}")
          copy_source_entry(entryPath, source_folder_path, replica_folder_path)
  # Deleting files and folders, if there not anymore in source folder
  for root, dirs, files in os.walk(replica_folder_path):
     allEntries = dirs + files
     for entryName in allEntries:
        destinationEntryPath = os.path.join(root, entryName)
        sourceEntryPath = create_source_path(destinationEntryPath, source_folder_path ,replica_folder_path)
        if not os.path.exists(sourceEntryPath):
           delete_destination_entry(destinationEntryPath)

if __name__ == "__main__":
    try:
        sync_interval, source_folder_path, replica_folder_path = verify_arguments(sys.argv)
        print(f"The synchronizer is running in interval {sync_interval} with source folder path: '{source_folder_path}' and replica folder path: '{replica_folder_path}'.")   
        while True:
            print("Running synchronization process!")
            compare_folder_content(source_folder_path, replica_folder_path)
            time.sleep(sync_interval)
    except ValueError as ve:
        print(f"Error: {ve}")
    except KeyboardInterrupt:
        print("\nSynchronizer terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")



