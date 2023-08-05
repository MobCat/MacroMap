#!/env/Python3.10.4
#/MobCat (2023)

import os

def process_md5translate_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        print(f"Working on {len(lines)} map files, please wait..")

    for line in lines:
        line = line.strip()
        if line.startswith("dir: "):
            continue

        parts = line.split("\t")
        if len(parts) != 2:
            continue

        source_file_path, md5_file_name = parts

        # Split the source_file_path into directory and file name
        directory, file_name = os.path.split(source_file_path)

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
    try:
        process_md5translate_file("md5translate.trs")
    except FileNotFoundError:
        print("md5translate.trs file not found in Minimap folder.")
        exit()
    os.remove("md5translate.trs")
    print("Done.")
