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

def verifyArguments(passedArguments):
   EXPECTED_NUMBER_OF_ARGUMENTS = 3
   cleansedArguments = passedArguments[1:]
   if len(cleansedArguments) == EXPECTED_NUMBER_OF_ARGUMENTS:
      interval, sourceFolderPath, replicaFolderPath = cleansedArguments
      try:
         interval = int(interval)
         validatePath(sourceFolderPath)
         validatePath(replicaFolderPath)
         return interval, sourceFolderPath, replicaFolderPath
      except ValueError as ve:
        print(f"Error: {ve}")
      except Exception as e:
        print(f"Unexpected error: {e}")   
   else:
      print("Invalid number of values passed! Check number of paramaters and run application again.")

def validatePath(path):
       if not os.path.exists(path):
        raise ValueError(f"Path: {path} does not exist.")
       if not os.path.isdir(path):
        raise ValueError(f"Path: {path} is not a directory.")
       
def copySourceEntry(sourceEntryPath, sourceFolderPath, replicaFolderPath):
  try:
    destinationPath = createDestinationPath(sourceEntryPath, sourceFolderPath, replicaFolderPath)
    if os.path.isfile(sourceEntryPath):
      shutil.copy2(sourceEntryPath, destinationPath)
    elif os.path.isdir(sourceEntryPath):
      shutil.copytree(sourceEntryPath, destinationPath)
    logging.info(f"Copied: {sourceEntryPath} to {destinationPath}")
    print(f"Copied: {sourceEntryPath} to {destinationPath}")
  except Exception as e: 
        logging.error(f"Error copying {sourceEntryPath} to {destinationPath}: {str(e)}")
        print(f"Error: {str(e)}")

def deleteDestinationEntry(destinationEntryPath):
  try:
    if os.path.isfile(destinationEntryPath):
      os.remove(destinationEntryPath)
    elif os.path.isdir(destinationEntryPath):
      shutil.rmtree(destinationEntryPath)
    logging.info(f"Deleted: {destinationEntryPath}")
    print(f"Deleted: {destinationEntryPath}")
  except Exception as e: 
        logging.error(f"Error deleting {destinationEntryPath}: {str(e)}")
        print(f"Error: {str(e)}")

def createDestinationPath(sourcePath, sourceFolderPath, replicaFolderPath):
  return sourcePath.replace(sourceFolderPath, replicaFolderPath)

def createSourcePath(destinationPath, sourceFolderPath, replicaFolderPath):
   return destinationPath.replace(replicaFolderPath, sourceFolderPath)

# This function verifies whether the content of a file remains consistent and is utilized to replace files if the content is not identical
def getFileHash(filePath):
   hasher = hashlib.md5()
   with open(filePath, "rb") as file:
      buf = file.read()
      hasher.update(buf)
   return hasher.hexdigest()

def compareFileContent(entryPath, destinationEntryPath):
   return getFileHash(entryPath) != getFileHash(destinationEntryPath)

def compareFolderContent(sourceFolderPath, replicaFolderPath):
  # Copying files and folders to replica directory, if new file or folder will appear in source directory
  for root, dirs, files in os.walk(sourceFolderPath):
     allEntries = dirs + files
     for entryName in allEntries:
        entryPath = os.path.join(root, entryName)
        destinationEntryPath = createDestinationPath(entryPath, sourceFolderPath, replicaFolderPath)
        # Comparing file content by hash must be second, because the file needs to exists first.
        if not os.path.exists(destinationEntryPath) or (os.path.isfile(entryPath) and compareFileContent(entryPath, destinationEntryPath)):
          copySourceEntry(entryPath, sourceFolderPath, replicaFolderPath)
  # Deleting files and folders, if there not anymore in source folder
  for root, dirs, files in os.walk(replicaFolderPath):
     allEntries = dirs + files
     for entryName in allEntries:
        destinationEntryPath = os.path.join(root, entryName)
        sourceEntryPath = createSourcePath(destinationEntryPath, sourceFolderPath ,replicaFolderPath)
        if not os.path.exists(sourceEntryPath):
           deleteDestinationEntry(destinationEntryPath)

if __name__ == "__main__":
    try:
        SYNC_INTERVAL, SOURCE_FOLDER_PATH, REPLICA_FOLDER_PATH = verifyArguments(sys.argv)
        print(f"The synchronizer is running in interval {SYNC_INTERVAL} with source folder path: '{SOURCE_FOLDER_PATH}' and replica folder path: '{REPLICA_FOLDER_PATH}'.")   
        while True:
            print("Running synchronization process!")
            compareFolderContent(SOURCE_FOLDER_PATH, REPLICA_FOLDER_PATH)
            time.sleep(SYNC_INTERVAL)
    except ValueError as ve:
        print(f"Error: {ve}")
    except KeyboardInterrupt:
        print("\nSynchronizer terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")



