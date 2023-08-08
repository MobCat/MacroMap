#!/env/Python3.10.4
#/MobCat (2023)

import subprocess
import os
import ctypes
import shutil

def runScript(inputFile):
	# Get the current directory where the main_script.py is located
	current_dir = os.path.dirname(os.path.abspath(__file__))

	# Define the path to the other_script.py in the same folder
	other_script_path = os.path.join(current_dir, inputFile)

	try:
		# Run the other_script.py using subprocess
		subprocess.run(["python", other_script_path], check=True)
	except subprocess.CalledProcessError as e:
		print(f"Error occurred while running {inputFile}: {e}")

if __name__ == "__main__":
	runScript("md5Fix.py")
	runScript("macroMap.py")
	runScript("MoveMacroMap.py")

	#Cleanup if you only wanted the macroMaps and not the converted or leftover tiles
	#shutil.rmtree("Minimap")
