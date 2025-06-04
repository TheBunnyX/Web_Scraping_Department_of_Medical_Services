import pandas as pd
import xlsxwriter
import openpyxl

df = pd.read_excel("testdelrow.xlsx")
"""
test = 0
for round_num in range(3): 
    if(round_num == 0):
        start_row = round_num*(50 + test)
        end_row = start_row + 36
        df = df.drop(df.index[start_row:end_row])
        test + 1
    else:
        start_row = round_num*(50 + test)
        end_row = start_row + 38
        df = df.drop(df.index[start_row:end_row])
        test + 1
"""        
df = df.drop_duplicates(subset = [4])  #correct

df = df.drop(df.columns[[0,2, 3,6,7,9,11,12,13,15]],axis = 1)
#df.drop_duplicates(df[5])

df.to_excel("testdelrow1.xlsx", index = False)