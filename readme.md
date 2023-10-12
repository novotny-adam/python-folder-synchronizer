# Python folder synchronizer

This program synchronizes two folders: the main folder, known as the "source," and a secondary folder called the "replica." It transfers files and folders from the source to the replica. If a file or folder is deleted from the source, it is also deleted from the replica. If the content of a file changes, the corresponding file in the replica folder will be updated. Every action that takes place is logged to both the file `synchronizer-actions.log` and the console.

## How to run

1. Navigate to the project directory
2. Execute command `python python-folder-synchronizer.py [SYNC_INTERVAL] [SOURCE_FOLDER_PATH] [REPLICA_FOLDER_PATH]`

   Replace:

- [SYNC_INTERVAL] with the desired synchronization interval in seconds.
- [SOURCE_FOLDER_PATH] with the path to the source folder.
- [REPLICA_FOLDER_PATH] with the path to the replica folder.

3. Synchronization will be started! 🎉

### Parameters

`[SYNC_INTERVAL]`

- **Type**: Integer
- **Description**: The time, in seconds, between each synchronization check. For instance, if 10 is specified, the program will check for changes in the source folder and update the replica folder accordingly every 10 seconds.

`[SOURCE_FOLDER_PATH]`

- **Type**: String
- **Description**: The path to the source folder. Changes in this folder will be tracked and replicated in the replica folder. Ensure that the path is valid and that the folder exists to avoid errors.
- **Examples**:
  - source/ (When is folder in root directory with program)
  - /Users/novotad/Desktop/original (Absolute path, when folder is somewhere else in the system)

`[REPLICA_FOLDER_PATH]`

- **Type**: String
- **Description**: The path to the replica folder. This folder will be synchronized to mirror the contents of the source folder based on the specified interval. Ensure that the path is valid and that the folder exists to prevent synchronization issues.
- **Examples**:
  - replica/ (When is folder in root directory with program)
  - /Users/novotad/Desktop/backup (Absolute path, when folder is somewhere else in the system)
