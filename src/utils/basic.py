import glob

def get_folder_files(foldername, pattern = '*'):
    return glob.glob(foldername + pattern)