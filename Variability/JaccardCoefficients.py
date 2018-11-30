#! python3

from __future__ import print_function
from collections import OrderedDict

class FormatDF(object):

    FLOAT_LIST = ['float', 'float32', 'float64',]
    INT_LIST = ['int', 'int32', 'int64',]


    def __init__(self, data_frame):
        self.df = data_frame
        self.__type_dict(self.df)


    def __str__(self):
        return f'Class: \'<{self.__class__.__name__}>\''


    def __type_dict(self, df = None):
        self.type_dic = OrderedDict()
        for i in df:
            self.type_dic[i] = df[i].dtype
        self.__find_numeric()


    def __find_numeric(self):
        full_list = self.FLOAT_LIST + self.INT_LIST
        self.numeric_dic = {i:self.type_dic[i] for i in self.type_dic.keys() if self.type_dic[i] in full_list}


    def clean_data(data_frame, print_nan_count=False):
        """ Will convert int to float and fill nan with zero. """
        self.numeric_dic = self.__find_numeric()
        df = data_frame.copy(deep = True)
        if print_nan_count:
            print(f'Null values found in each column:\n{df.isna().sum()}')
        else:
            df = df_1.fillna(0)
            for i in df.select_dtypes(include=['int64']):
                df[i] = df[i].astype(float)
            return df




class Jaccard(object):
    """
    Find Jaccard coefficients, return results to dataframe.

    Example usage:
        >>> from FindJaccard import *
        >>> jac = Jaccard()
        >>> df3 = jac.calc_jaccard(data_frame)
    """
    def __init__(self, data_frame=None):
        self.df = data_frame
        if not self.df is None:
            self.calc_jaccard()

    
    def __set_values(self):
        self.column_list = self.df.columns.values.tolist()
        self.row_list = self.df.index.values.tolist()


    def calc_jaccard(self, data_frame=None):
        if not data_frame is None:
            self.df = data_frame
        self.__set_values()
        self.df = self.df.reindex(index = self.row_list, columns = self.column_list)
        for i in self.column_list:
            for j in self.row_list:
                if i == j or self.df.loc[i, j] == 0:
                    self.df.loc[i, j] = 0.0
                else:
                    self.df.loc[i, j] = self.df.loc[i, j] / (self.df.loc[i, i] + self.df.loc[j, j])
        return self.df.iloc[:,:]

    def print_sample_results(self, df=None, columns=0, rows = 0):
        if not df is None:
            self.calc_jaccard(df)
        try:
            if columns == 0 and rows == 0:
                print(f'{self.df.head()}')
            elif columns > 0 and rows > 0:
                print(f'{self.df.iloc[:rows, :columns]}')
            elif columns == 0 and rows > 0:
                print(f'{self.df.iloc[:rows, :]}')
            elif columns > 0 and rows == 0:
                print(f'{self.df.iloc[:, :columns]}')
        except ValueError:
            print('Data frame needed to run print function!')
