#!/usr/bin/python

import sys, getopt, os
from dotenv import load_dotenv
load_dotenv(verbose=False)
sys.path.append(os.getenv("ROOT_DIR"))
from utils import basic

def main(argv):
   inputfolder = ''
   table = ''
   try:
      opts, arg = getopt.getopt(argv,"hi:t:",["ifolder=","tab="])
   except getopt.GetoptError:
      print('upload.py -i <inputfolder> -t <table>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('upload.py -i <inputfolder> -t <table>')
         sys.exit()
      elif opt in ("-i", "--ifolder"):
         inputfolder = arg
      elif opt in ("-t", "--tab"):
         table = arg
   print('Input folder is "' + inputfolder + '"')
   print('Table is "' + table + '"')
   print(basic.get_folder_files(inputfolder))

if __name__ == "__main__":
   main(sys.argv[1:])