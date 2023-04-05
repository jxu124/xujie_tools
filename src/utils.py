# Author: Xu Jie
# Date: 4/5/2023

import os
import zipfile
import logging
from tqdm.notebook import tqdm


logger = logging.getLogger(__name__)


class ZipDataset():
    """
    The code defines a class called ZipDataset that can be used to read data from a zip file. 
    The __init__ method opens the zip file and stores the names of the files in the namelist attribute. 
    The get method reads the contents of a file from the zip file and returns it as a string. 
    The get_fp method returns a file object for the specified file in the zip file. 
    The close method closes the zip file.

    Here is a more detailed explanation of each method:
    __init__ method: This method opens the zip file and stores the names of the files in the namelist attribute. 
        It also prints a message to the console indicating that the zip file is being loaded.
    get method: This method reads the contents of a file from the zip file and returns it as a string. 
        It also prints a message to the console indicating that the file is being read.
    get_fp method: This method returns a file object for the specified file in the zip file.
    close method: This method closes the zip file. It also prints a message to the console indicating 
        that the zip file is being closed.

    Here is an example of how to use the ZipDataset class:

    import zipfile

    # Create a `ZipDataset` object for the zip file `data.zip`.
    dataset = ZipDataset('data.zip')

    # Get the contents of the file `file1.txt` from the zip file.
    data = dataset.get('file1.txt')

    # Print the contents of the file.
    print(data)

    This code would print the contents of the file file1.txt from the zip file data.zip.
    """
    def __init__(self, filepath=0):
        print(filepath)
        logger.info(f"Load zipfile {filepath} start...")
        self.zf = zipfile.ZipFile(filepath)
        logger.info(f"Load zipfile {filepath} finished.")
        self.namelist = self.zf.namelist()

    def get(self, file):
        with self.zf.open(file) as f:
            data = f.read()
        return data

    def get_fp(self, file):
        return self.zf.open(file)

    def close(self):
        self.zf.close()


if __name__ == "__main__":
    ds = ZipDataset("/Users/bytedance/Downloads/dataset.zip")
    # print(ds.namelist)
    ds.close()
