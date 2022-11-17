# Copyright (c) 2022 Intel Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# SPDX-License-Identifier: MIT

import pandas as pd
import numpy as np

def separating_col_func(data_frame, separation_cols):
    if(data_frame.shape[0]==0):
        return data_frame
    df = 'dataframe_'
    max_cell_length = {}
    for colnames1 in separation_cols.split(','):
        cell_length = []
        data_frame[colnames1] = data_frame[colnames1].fillna("").apply(list)
        for i in range(data_frame.shape[0]):
            cell_length.append(len(data_frame[colnames1][i]))
        max_cell_length[colnames1] = max(cell_length)
        df_0 = df+colnames1
        df_0 = pd.DataFrame([[[] for i in range(max_cell_length[colnames1]-1)] for i in range(data_frame.shape[0])],columns=[colnames1+'_{}'.format(x) for x in range(1, max_cell_length[colnames1])])
        data_frame = pd.concat([data_frame, df_0], axis=1)
        for j in range(data_frame.shape[0]):
            for k in range(len(data_frame[colnames1][j])-1):
                back_it = data_frame.shape[1]-(k+1)
                data_frame.iloc[j, back_it] = data_frame[colnames1][j][k+1]
            if len(data_frame[colnames1][j]) != 0:
                data_frame[colnames1][j] = data_frame[colnames1][j][0]
    return data_frame


def explode_multiple(df1, list_cols):
    for colnames1 in list_cols:
        df1[colnames1] = df1[colnames1].fillna("").apply(list)
    df1['tmp'] = df1.apply(lambda row: list(zip(*(row[x] for x in list_cols))), axis=1)
    df1 = df1.explode('tmp')
    df1['tmp'] = df1['tmp'].fillna("").apply(list)
    df1[list_cols] = pd.DataFrame(df1['tmp'].tolist(), index=df1.index)
    df1.drop(columns='tmp', inplace=True)
    return df1

def equivalent_col_func(data_frame_2, equivalent_cols):
    cnti = 0
    for i in equivalent_cols.split(':'):
        if ':' in equivalent_cols:
            if cnti == 0:
                list1 = i.split(',')[:-1]
                cnti = cnti + 1
            else:
                list1 = i.split(',')
                list1.pop(0)
            data_frame_2 = explode_multiple(data_frame_2,list1)
            #data_frame_2 = data_frame_2.explode(list1)
        else:
            list1 = i.split(',')
            data_frame_2 = explode_multiple(data_frame_2,list1)
            #data_frame_2 = data_frame_2.explode(list1)
    return data_frame_2

def flattening(data_frame_2,equivalent_cols, not_flattening_cols):
    for colname, coltype in data_frame_2.dtypes.iteritems():
        if colname not in equivalent_cols.split(',') and colname != 'index' and colname not in not_flattening_cols.split(','):
                data_frame_2 = data_frame_2.explode(colname)

    return data_frame_2

def intersection_cols(data_frame_3,col_args):
    new_equiv_string = ''
    for i in col_args.split(','):
        if i in list(data_frame_3.columns.values):
            new_equiv_string = new_equiv_string+i+','
        elif i == ':':
            new_equiv_string = new_equiv_string+i+','
        else:
            print('Mismatch')
    if len(new_equiv_string) != 0:
        if new_equiv_string[-1] == ',':
            new_equiv_string = new_equiv_string[0:(len(new_equiv_string)-1)]
    return new_equiv_string