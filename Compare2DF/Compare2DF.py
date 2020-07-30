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
    df1 = pd.read_csv(dir_df1, sep=',', header=0, index_col=False, encoding='ANSI')
    df2 = pd.read_csv(dir_df2, sep=',', header=0, index_col=False, encoding='ANSI')
    df1 = df1.fillna(0)
    df2 = df2.fillna(0)
    col_df1 = list(df1.columns)
    col_df2 = list(df2.columns)
    if len(col_df1) == len(col_df2):
        if col_df1 == col_df2:
            index_df1 = df1.shape[0]  
            index_df2 = df2.shape[0]
            df_i = pd.DataFrame(columns=list(df1.columns))
            list_j = list(range(index_df2))
            for i in range(index_df1):
                bol = []
                # Se inicia bol_i en False, cambiara a True, si row i != row j
                bol_i = False                    
                for j in list_j:
                    bol = df1.loc[i,:] == df2.loc[j,:]         
                    bol_unique = bol.unique()
                    if len(bol_unique) == 1:
                        if bol_unique:
                            # i == j
                            # Eliminamos la row j y el valor j de la list_j
                            # Salimos del ciclo de comparación j
                            df2.drop(j,inplace=True)
                            list_j.remove(j)
                            bol_i=True
                            break
                        else:
                            bol_i = False
                    else:
                        bol_i = False
                if not bol_i:
                    df_i = df_i.append(df1.loc[i,:])
        else:
            for col in col_df1:
                if col in col_df2:
                    pass
                else:
                    print('La columna {} no existe en df2.'.format(col))
            print('El orden de las columnas no es identico.')
    else:
        print('Los archivos no tienen el mismo numero de columnas.')
    if df_i.empty:
        print('Todas las filas de df1 se encontraron en df2.')
    else:
        df_i.to_csv('df1.txt', ',')
        print('Se ha guardado un archivos con las filas de df1 que no se encontraron en df2.')
    if df2.empty:
        print('Todas las filas  de df2 se encontraron en df1.')
    else:
        df2.to_csv('df2.txt', sep=',')
        print('Se ha guardado un archivo con las filas de df2 que no se encontraron en df1.')
     
if __name__=='__main__':
    dir_df1 = 'PATH'
    dir_df2 = 'PATH'
    Compare2DF(dir_df1,dir_df2)