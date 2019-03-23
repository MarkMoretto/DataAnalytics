#! python3

""" 
This module extracts compressed files into a user-set directory. 

Example usage:
    >>> base_filename = 'miscfile.ver.1.0.1.tar.gz'
    >>> destination_directory = 'C:\...\path_to_directory_where_file_should_be_extracted' 
    >>> extract_file(base_filename, destination_directory)
"""

from __future__ import print_function

import os
import tarfile
import zipfile
import pandas as pd
from getpass import getuser


class ExtractionException(Exception):
    pass


class FileExtractionError(ExtractionException):
    pass


class MissingValueError(ExtractionException):
    fe_dic = {
        '123':'Error! Filename value needed for extraction.',
        '456':'Error! Destination directory value needed for extraction.',
        }


class FileExtensionError(ExtractionException):
    pass


class FileType(object):
    TAR_XZ = 'r:xz'
    TAR_GZ = 'r:gz'
    TAR_BZ = 'r:bz2'
    ZIPFILE = 'zip'
    GZIP = 'gzip'


class BaseExtractor(FileType):

    SOURCE_DIR = r'C:\Users\{}\Downloads'.format(getuser()).lower()
    FILENAME = r''
    DEST_DIR = r'C:\Users\{}\Desktop'.format(getuser()).lower()

    def __init__(self, file_name=None, destination_dir=None):
        super().__init__()
        if not destination_dir is None:
            self.DEST_DIR = destination_dir.lower()
        if not file_name is None:
            self.FILENAME = file_name.lower()
        self.format_filepath()
        self.extension = self.FILENAME.split('.')[-1]


    def format_filepath(self):
        self.full_path = os.path.join(self.SOURCE_DIR, self.FILENAME)


    def __get_extension(self):
        self.extension = self.FILENAME.split('.')[-1]


    def extract(self, output_filename=None):
        self.format_filepath()
        self.__get_extension()
        if self.extension == 'xz':
            xyz = tarfile.open(self.full_path, self.TAR_XZ)
            xyz.extractall(path=self.DEST_DIR)
        elif self.extension == 'bz2':
            xyz = tarfile.open(self.full_path, self.TAR_BZ)
            xyz.extractall(path=self.DEST_DIR)
        elif self.extension == 'zip':
            with zipfile.ZipFile(self.full_path) as xyz:
                xyz.extractall(self.DEST_DIR)
        elif self.extension == 'gz' or self.extension == 'tgz':
            self.subextension = '.'.join([i for i in self.FILENAME.split('.')[-2:]])
            if self.subextension == 'csv.gz':
                out_name = self.FILENAME.split('.')[0] + '.csv'
                if not output_filename is None:
                    full_out_pth = os.path.join(self.dest_dir, output_filename)
                    df = pd.read_csv(self.full_path, compression = self.GZIP, error_bad_lines = False)
                    df.to_csv(full_out_pth, index=False)
                else:
                    full_out_pth = os.path.join(self.dest_dir, out_name)
                    df = pd.read_csv(self.full_path, compression = self.GZIP, error_bad_lines = False)
                    df.to_csv(full_out_pth, index=False)
            else:
                try:
                    xyz = tarfile.open(self.full_path, self.TAR_GZ)
                    xyz.extractall(path = self.DEST_DIR)
                except:
                    raise FileExtensionError(f'Cannot process file with extension {self.subextension}.')

        try:
            xyz.close()
        except FileExistsError:
            pass


def extract_file(filename=None, dest_directory=None):
    ef = BaseExtractor()

    try:
        ef.FILENAME = filename
    except MissingValueError as me:
        print(f'{me.args[0]}: {me.fe_dic[me.args[0]]}')

    try:
        ef.DEST_DIR = dest_directory
    except MissingValueError as me:
        print(f'{me.args[1]}: {me.fe_dic[me.args[1]]}')

    try:
        ef.extract()
    except:
        raise FileExtractionError(f'Error extracting file {ef.FILENAME}.\nPlease check setings and rerun.')
