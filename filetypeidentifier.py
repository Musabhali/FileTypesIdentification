"""
Technological University Dublin - TUD
B00106732 Musab Hersi Ali
Module Name : Individual Project
Title: File Type Identification Through Computer Vision
Supervisor: Micheal Hegarty
"""

""" filetypeidentifier.py - Scan directory structure for defined 
	filetypes & convert them to byteplot .pdf format, saving them in
	new 'scanned_files' folder """
import os, numpy as np, colorama
from PIL import Image
from array import array
from train_test import identify , report_gen
import argparse

#GLOBALS
FILETYPES = (".pdf", ".exe", ".html", ".jpg", ".dll")
WIDTH = 256 #WIDTH IS ALWAYS 256

def binary_convert(fp, filename):
	""" Convert and Save file as .png 
		@param: <str>fname - filename
	"""
	with open(fp, "rb") as f:
		f_length = os.path.getsize(fp) #Length of file in bytes
		print(f"{f_length} Bytes")
		
		if f_length < WIDTH:
			print("FILE TOO SMALL TO CONVERT! (less than 256 Bytes)\n")
			return None #Skip conversion of file
		
		rem = f_length % WIDTH
		f_arr = array("B") #int array
		f_arr.fromfile(f, f_length - rem)
		val = int((len(f_arr) / WIDTH))
		
		g = np.reshape(f_arr, (val, WIDTH))
		m = Image.fromarray(g)
		
		#Save converted files in the scanned_files directory
		#directory = r".\files\scanned_files" #dir to save to
		directory = r".\files\scanned_files" #dir to save scanned files for identification
		m.save(f"{directory}\{filename}.png")
		print("Coverted & Saved a copy as .png!\n")

def dir_scan(path):
	"""	Scan directory to Get all files of given type(s)
		@param: <str>path - path to directory (relative or full path)
	"""
	print(f"Searching {path}...\n")
	for dirpath, dirs, files in os.walk(path, onerror=1):
		#Recursive search through given directory
		print \
		(colorama.Fore.LIGHTRED_EX, f'\nDIRECTORY: {dirpath}', end='')
		print(colorama.Style.RESET_ALL) #reset terminal color
		
		for xt in range(5): #Iterate for each filetype		
			for filename in files: #Check file extensions
				if(filename.lower()).endswith(FILETYPES[xt]):
					fp = os.path.join(dirpath, filename) #path+fname
					print(colorama.Fore.LIGHTYELLOW_EX, fp)
					binary_convert(fp, filename)
					print(colorama.Style.RESET_ALL)

if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-d", "--dir", required=True, help="path to the folder to scan")
	colorama.init() #Used for coloring terminal text 

	args = vars(ap.parse_args())
	#dir_in = r".\files\originalFilesForTesting"
	
	dir_scan(args["dir"])
	try:
		#dir_in = input("Copy & Paste Directory to Search:")
		dir_scan(args["dir"]) #Scan & convert original files
		print(colorama.Back.WHITE, colorama.Fore.LIGHTBLUE_EX, \
		"Creating & Training Machine Model to Predict File Type...")
		print(colorama.Style.RESET_ALL)
		identify()
		report_gen()
	
	except TypeError:
		print(f"ERROR -> {args} No Such Directory Found...")
		exit(1)