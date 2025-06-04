import pandas as pd
data0 = {
    'A': [1, 6, 11, 6, 11],
    'B': [6, 6, 6, 6, 11],
    'C': [3, 8, 13, 6, 11],
    'D': [4, 9, 14, 6, 11],
    'E': [5, 10, 3, 20, 0]
}

data1 = {
    'A': [1, 6, 11, 6, 11],
    'B': [6, 6, 6, 6, 11],
    'C': [3, 8, 13, 6, 11],
    'D': [4, 9, 14, 6, 11],
    'E': [5, 10, 15, 6, 11]
}

data2 = {
    'A': [16, 21, 26, 31, 26],
    'B': [10, 50, 10, 50, 26],
    'C': [18, 23, 28, 33, 1],
    'D': [4, 9, 14, 4, 26],
    'E': [20, 25, 10, 5, 26]
}

data3 = {
    'A': [1, 6, 11, 6, 11],
    'B': [6, 6, 6, 6, 12],
    'C': [3, 8, 13, 6, 11],
    'D': [4, 9, 14, 6, 11],
    'E': [10, 5, 30, 5, 10]
}

data4 = {
    'A': [1, 6, 11, 6, 11],
    'B': [6, 6, 6, 6, 11],
    'C': [3, 8, 13, 6, 11],
    'D': [4, 9, 14, 6, 11],
    'E': [10, 25, 30, 5, 26]
}



df0 = pd.DataFrame(data1)
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df3 = pd.DataFrame(data3)
df4 = pd.DataFrame(data4)

df = pd.concat([df1, df2, df3, df4], ignore_index = True) #รวม

df5 = df.drop_duplicates(subset = ["E"])  #correct

#df2 = df2[~df2.iloc[:, 4].isin(duplicates) & ~df3.iloc[:, 4].isin(duplicates) & ~df4.iloc[:, 4].isin(duplicates)]
df6 = df5[~df5["E"].isin(df0["E"])]   #เหลือ


df7 = pd.concat([df0,df6], ignore_index = True) #รวม

print("df0 = \n",df0)
#print("df1 = \n",df1)
#print("df2 = \n",df2)
#print("df3 = \n",df3)
#print("df4 = \n",df4)
print("df5 = \n",df5)
print("df5-df0 = \n",df6)
print("df7 = \n",df7)
