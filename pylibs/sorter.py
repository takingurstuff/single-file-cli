import os
import glob
import shutil

sitefolder = "/Volumes/T0/threads"
tmpdls = "/Volumes/T0/sftmpdl"
blocks = {}


def sort(block, title):
    sitecreated = os.path.exists(sitefolder)
    if not sitecreated:
        os.mkdir(sitefolder)

    if block not in blocks:
        blockpath = os.path.join(sitefolder, block)
        blocks[block] = blockpath
        os.mkdir(blockpath)

    threadfolder = os.path.join(sitefolder, blockpath, title)
    if not os.path.exists(threadfolder):
        os.mkdir(threadfolder)

    search_path = os.path.join(tmpdls, "*.*")

    # Use glob to find files matching the pattern
    files_to_copy = glob.glob(search_path)

    for file_path in files_to_copy:
        # Get the base name of the file
        file_name = os.path.basename(file_path)

        # Create the full path for the target file
        target_file_path = os.path.join(threadfolder, file_name)

        # Copy the file to the target directory
        shutil.copy(file_path, target_file_path)
        print(f"Copied: {file_path} to {target_file_path}")
