#!/usr/bin/python

import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic
from db.delta_upload import DeltaUploader


def main(argv):
   inputfolder = ''
   table = ''
   try:
      opts, arg = getopt.getopt(argv,"hi:",["ifolder="])
   except getopt.GetoptError:
      print('upload.py -i <inputfolder>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('upload.py -i <inputfolder>')
         sys.exit()
      elif opt in ("-i", "--ifolder"):
         inputfolder = arg
   print('Input folder is "' + inputfolder + '"')

   file_list = basic.get_folder_files(inputfolder)
   print("Following files were found: " + str(file_list))
   _DeltaUploader = DeltaUploader()

   for filepath in file_list:
      print("Import " + filepath + " to DB.")
      try:
         _DeltaUploader.delta_upload(filepath)
         print("Done.")
      except:
         print("Import of " + filepath + " has failed.")

if __name__ == "__main__":
   main(sys.argv[1:])