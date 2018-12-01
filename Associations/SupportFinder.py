#! python3

"""
Module for finding support levels for data pairs in market basket analysis.

Dataframe argument should be formatted with item names as column headers and index values. Values should be floating point,
but integer values might work.

Sample dataframe:
      A   B   C
  A  1.0 2.0 2.0
  B  2.0 4.0 1.0
  C  1.0 1.0 5.0


Module Exceptions:
    DataException()
    GeneralDataError()

Module Classes:
    FindSupport()
"""

import sys
import pandas as pd


class DataException(Exception):
    pass


class GeneralDataError(DataException):
    def __init__(self):
        super().__init__()
        self.instance_info = sys.exc_info()[0]
        self.err_msg = sys.exc_info()[2]

    def print_err(self):
        return f'Exception instance:\n\t{self.instance_info}\nError message:\n\t{self.err_msg}'


class FindSupport(object):

    """
    Example usage:
    >>> fs = FindSupport(data_frame = df1)
    >>> supportDF = fs.support_df

    Anodhter example:
    >>> support_df = FindSupport(data_frame = df1).support_df
    """

    def __init__(self, data_frame=None):
        self.count_dict = dict()
        self.support_dict = dict()
        self.total_count = 0
        try:
            self.df = data_frame.copy(deep=True)
            self.create_count_dict(data_frame)
            self.get_support_data()
        except GeneralDataError as ge:
            ge.print_err()

    def create_count_dict(self, data_frame = None):
        self.df = data_frame.copy(deep=True)
        col_list = self.df.columns.values.tolist()
        idx_list = self.df.index.values.tolist()

        for i in col_list:
            for j in idx_list:
                if i == j:
                    self.count_dict[i] = self.df.loc[i, j]



    def __get_total_count(self):
        if len(self.count_dict.keys()) > 0:
            self.total_count = sum(self.count_dict.values())


    def create_support_dict(self):
        self.__get_total_count()
        try:
            if self.total_count > 0:
                for k in self.count_dict.keys():
                    self.support_dict[k] = round(self.count_dict[k] / self.total_count, 6)

        except GeneralDataError as ge:
            ge.print_err()


    def get_support_data(self):
        try:
            if len(self.support_dict.keys()) == 0:
                self.create_support_dict()
                new_dict = dict()
                new_dict['Items'], new_dict['Support Level']  = zip(*self.support_dict.items())
            self.support_df = pd.DataFrame().from_dict(data = new_dict)
        except GeneralDataError as ge:
            ge.print_err()
