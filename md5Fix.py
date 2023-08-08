#!/env/Python3.10.4
#/MobCat (2023)

import os
import shutil # Because OS move sucks.

def process_md5translate_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        # This counter is not excat as it will incude newline and the 'dir: Azeroth' but its good enough to give the user an idea
        # of how many files we are translateing
        print(f"Working on {len(lines)} map tiles, please wait..")

    for line in lines:
        line = line.strip()
        if line.startswith("dir: "):
            continue

        parts = line.split("\t")
        # Check if the map has a zone name
        if len(parts) != 2:
            continue
        #else:
            # Fix for beta map files in the root of the folder structer.
            #parts[0] = 'Root\\' + parts[0]

        source_file_path, md5_file_name = parts

        # Split the source_file_path into directory and file name
        directory, file_name = os.path.split(source_file_path)
        # hotfox for beta map files in the root of the folder structer.
        if len(directory) == 0:
            directory = "!Root"

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Rename the md5 file to the original file name
        try:
        	os.rename(md5_file_name, os.path.join(directory, file_name))
        except FileExistsError:
            os.remove(os.path.join(directory, file_name)) # Kinda poopie fix for if files excists replace it.
            os.rename(md5_file_name, os.path.join(directory, file_name))
        except FileNotFoundError:
            # Sometimes there are files listed in the md5 list that dont excist anymore, or yet. So we just skip them for now.
        	continue

if __name__ == "__main__":
    os.chdir("Minimap")

    # Check for beta or wow 1 md5translate.txt
    # Copy it from Data\textures\Minimap\md5translate.txt folder in the games dir.
    if os.path.exists("md5translate.trs"):
        workFile = "md5translate.trs"
    elif os.path.exists("md5translate.txt"):
        print("md5translate.trs file not found in Minimap folder.\nLooking for beta WoW md5translate.txt file")
        workFile = "md5translate.txt"
    else: # No md5 translate file found.
        print("ERROR: No md5translate file was found in Minimap folder.")
        exit()

    # Now we have the file, procuess it.
    process_md5translate_file(workFile)

    # Cleanup
    os.remove(workFile)
    # Let a list of all left over unstanslated files
    leftOvers = [f for f in os.listdir() if os.path.isfile(os.path.join(os.getcwd(), f))]
    if len(leftOvers) > 0:
        realTiles = []
        brokenPatchTiles = []

        # Build a list of file based on the size
        for file in leftOvers:
            file_path = os.path.join(os.getcwd(), file)
            file_size = os.path.getsize(file_path)
    
            if file_size > 1:
                realTiles.append(file)
            elif file_size <= 1:
                brokenPatchTiles.append(file)

        # Delete all the bad tiles
        for file in brokenPatchTiles:
            file_path = os.path.join(os.getcwd(), file)
            os.remove(file_path)

        # Move all the good ones.
        if len(realTiles) != 0:
            new_folder_path = os.path.join(os.getcwd(), '!Unknown')
            if not os.path.exists(new_folder_path):
                os.mkdir(new_folder_path)
    
            for file in realTiles:
                source_path = os.path.join(os.getcwd(), file)
                destination_path = os.path.join(new_folder_path, file)
                shutil.move(source_path, destination_path)

        print("WARNING: Found untranslated files")
        print(f"Found {len(brokenPatchTiles)} blank title data")
        print(f"Found {len(realTiles)} that could not be translated")
        print("Blank files where removed, but untranslated files where moved to the !Unknown folder if they excisted in this translation.")

    print("Done.")
