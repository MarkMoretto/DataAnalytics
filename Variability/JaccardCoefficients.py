#! python3

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
