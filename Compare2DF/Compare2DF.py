'''
Este script toma dos archivos csv que pueden estar en distintas ubicaciones, los convierte en Dataframes
mediante la libreria pandas, verifica que tengan el mismo nombre y numero de columnas, luego los 
compara entre sí, generando en el directorio donde se ubica el script dos posibles archivos, uno con
las filas que no se encontraron del primer archivo en el segundo, y el segundo archivo, de las filas 
que estan en el segundo archivo pero no el primero. Se consideran CVS que tienen la primera fila los 
nombres de las columnas.
Trabaja con python 3.7
'''
import os

import pandas as pd

def Compare2DF(dir_df1,dir_df2):
    # dir_df1 ubicación del archivo df1.
    # dir_df2 ubicación del archivo df2.

    if header_:
        head = 0
        head_out = True
    else:
        head = None
        head_out = False

    df1 = pd.read_csv(dir_df1, sep=separ, header=head, index_col=False, encoding='ANSI')
    df2 = pd.read_csv(dir_df2, sep=separ, header=head, index_col=False, encoding='ANSI')
    df1 = df1.fillna(0)
    df2 = df2.fillna(0)
    col_df1 = list(df1.columns)
    col_df2 = list(df2.columns)
    if len(col_df1) == len(col_df2):
        if col_df1 == col_df2:
            df_l = pd.merge(df1, df2, how='outer',indicator=True).query('_merge == "left_only"').drop(columns=['_merge'])
            df_l.index += 1
            df_l = df_l.reset_index()
            df_l['index'] = 'Row: ' + df_l['index'].astype(str)
            df_r = pd.merge(df2, df1, how='outer',indicator=True).query('_merge == "right_only"').drop(columns=['_merge'])
            df_r.index += 1
            df_r = df_r.reset_index()
            df_r['index'] = 'Row: ' + df_r['index'].astype(str)
        else:
            for col in col_df1:
                if col in col_df2:
                    pass
                else:
                    print('La columna {} no existe en df2.'.format(col))
            print('El orden de las columnas no es identico.')
    else:
        print('Los archivos no tienen el mismo numero de columnas.')
    if df_l.empty:
        print('Todas las filas de df1 se encontraron en df2.')
    else:
        df_l.to_csv('df1.txt', sep=separ, header=head_out)
        print('Se ha guardado un archivos con las filas de df1 que no se encontraron en df2.')
    if df_r.empty:
        print('Todas las filas  de df2 se encontraron en df1.')
    else:
        df_r.to_csv('df2.txt', sep=separ, header=head_out)
        print('Se ha guardado un archivo con las filas de df2 que no se encontraron en df1.')


if __name__=='__main__':
    header_ = True
    separ = ','
    dir_df1 = 'PATH'
    dir_df2 = 'PATH'
    Compare2DF(dir_df1, dir_df2)
