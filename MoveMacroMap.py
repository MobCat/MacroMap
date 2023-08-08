#!/env/Python3.10.4
#/MobCat (2023)

import os
import re
import shutil

def find_and_move_files(base_folder, dest_folder):
    # Create the destination folder if it doesn't exist
    os.makedirs(dest_folder, exist_ok=True)

    # Define the regex pattern to match the desired files
    pattern = r'^!(.*)-MacroMap\.png$'

    for root, _, files in os.walk(base_folder):
        for filename in files:
            match = re.match(pattern, filename)
            if match:
                # Get the full path of the source file
                source_path = os.path.join(root, filename)

                # Extract the desired part of the filename
                new_filename = match.group(1) + ".png"

                # Move the file to the destination folder
                shutil.move(source_path, os.path.join(dest_folder, new_filename))

if __name__ == "__main__":
    base_folder = "Minimap"

    if not os.path.exists("MacroMap"):
        print(f"Making new MacroMap folder")
        os.makedirs("MacroMap")

    print("Moveing macroMaps to base folder...")
    find_and_move_files(base_folder, "MacroMap")
