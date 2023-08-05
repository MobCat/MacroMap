#!/env/Python3.10.4
#/MobCat (2023)

from PIL import Image
import os
import sys
import subprocess

def compile_images(folder_path, output_path):
    # Get a list of all PNG files in the folder
    png_files = [filename for filename in os.listdir(folder_path) if filename.lower().endswith('.png')]

    # Determine the minimum and maximum x and y values
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for filename in png_files:
        x = int(filename.split('_')[0].split('map')[1])
        y = int(filename.split('_')[1].split('.')[0])
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    # Calculate the grid size
    grid_width = (max_x - min_x + 1) * 256
    grid_height = (max_y - min_y + 1) * 256

    # Create the large PNG canvas
    canvas = Image.new('RGBA', (grid_width, grid_height), (0, 0, 0, 0))

    # Fill the canvas with transparent tiles for missing tiles
    transparent_tile = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            tile_filename = f"map{y:02d}_{x:02d}.png"
            tile_path = os.path.join(folder_path, tile_filename)
            if not os.path.exists(tile_path):
                canvas.paste(transparent_tile, ((x - min_x) * 256, (y - min_y) * 256))

    # Place the actual tiles on the canvas
    for filename in png_files:
        x = int(filename.split('_')[0].split('map')[1])
        y = int(filename.split('_')[1].split('.')[0])
        tile_filename = os.path.join(folder_path, filename)
        tile = Image.open(tile_filename)
        canvas.paste(tile, ((x - min_x) * 256, (y - min_y) * 256))

    # Save the final compiled image
    canvas.save(output_path)

def convert_images(folder_path, output_path):
    # Get a list of all PNG files in the folder
    blp_files = [filename for filename in os.listdir(folder_path) if filename.lower().endswith('.blp')]
    countblp = 1
    maxblp = len(blp_files)
    for filename in blp_files:
        # Chuck each blp file at the converter one folder up
        # and output them into the map folder
        print(f" [{countblp}/{maxblp}]", end="\r") # May not be compatibal with windows CMD. Try end="" if it fubars.
        subprocess.run(["../BLPConverter.exe", f"{folder_path}/{filename}"], stdout=subprocess.DEVNULL)
        os.remove(f"{folder_path}/{filename}")
        countblp += 1

########################################################################################################################
if __name__ == "__main__":
    os.chdir("Minimap")

	# Build a list of all the folders in our minimap folder.
    folders = [folder for folder in os.listdir(os.getcwd()) if os.path.isdir(os.path.join(os.getcwd(), folder))]
    folders.remove("WMO") # Hotfix, remove builds as they are not gridbased so the compile_images() rebuilder does not work.

    # setup for progress counter
    maxLen = len(folders)
    count = 1

    # convert each blp to png and delete blp when done
    for i in folders:
        print(f"\n({count}/{maxLen} {int((count/maxLen)*100)}%)Converting {i}")
        convert_images(i, i)
        count += 1 

    # build each folder of png grids into one big ass png file
    print('''\n####
Done
####''')
    count = 1
    for i in folders:
    	print(f"({count}/{maxLen} {int((count/maxLen)*100)}%)Building {i}")
    	try:
    		compile_images(i, f"{i}/!{i}-MacroMap.png")
    	except ValueError: # Shity fix
    		print("ERROR: Empty folder?")
    	count += 1

    print("Done.")
