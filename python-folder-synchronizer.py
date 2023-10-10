import os 
import shutil
import logging
import hashlib # Library for comparison of files by md5 hash

# Logging to file
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

SYNC_INTERVAL = 300 # Time in seconds
SOURCE_FOLDER_PATH = "source/"
REPLICA_FOLDER_PATH = "replica/"

def copySourceEntry(sourceEntryPath):
  try:
    destinationPath = createDestinationPath(sourceEntryPath)
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

def createDestinationPath(sourcePath):
  return sourcePath.replace(SOURCE_FOLDER_PATH, REPLICA_FOLDER_PATH)

def createSourcePath(destinationPath):
   return destinationPath.replace(REPLICA_FOLDER_PATH, SOURCE_FOLDER_PATH)

# This function verifies whether the content of a file remains consistent and is utilized to replace files if the content is not identical
def getFileHash(filePath):
   hasher = hashlib.md5()
   with open(filePath, "rb") as file:
      buf = file.read()
      hasher.update(buf)
   return hasher.hexdigest()



def compareFolderContent():
  # Copying files and folders to replica directory, if new file or folder will appear in source directory
  for root, dirs, files in os.walk(SOURCE_FOLDER_PATH):
     allEntries = dirs + files
     for entryName in allEntries:
        entryPath = os.path.join(root, entryName)
        destinationEntryPath = createDestinationPath(entryPath)
        isSameFileContent = getFileHash(entryPath) != getFileHash(destinationEntryPath)
        if not os.path.exists(destinationEntryPath) or isSameFileContent:
          copySourceEntry(entryPath)
  # Deleting files and folders, if there not anymore in source folder
  for root, dirs, files in os.walk(REPLICA_FOLDER_PATH):
     allEntries = dirs + files
     for entryName in allEntries:
        destinationEntryPath = os.path.join(root, entryName)
        sourceEntryPath = createSourcePath(destinationEntryPath)
        if not os.path.exists(sourceEntryPath):
           deleteDestinationEntry(destinationEntryPath)


compareFolderContent()


