import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import pandas as pd
def g(df):
  """
  ฟังก์ชันแปลง Column ที่ 5 ของ DataFrame Pandas เป็น Plain Text แยกตัวอักษรภาษาอังกฤษและ -

  Args:
    df: DataFrame Pandas

  Returns:
    DataFrame Pandas: DataFrame ใหม่ที่มี column เพิ่มเติม
  """
  df["Column 6"] = ""
  for i in range(df.shape[0]):
    # แยกตัวอักษรภาษาอังกฤษและ - จาก column ที่ 5
    text = ""
    col5 = df.loc[i, 5]
    if isinstance(col5, str):
      for char in col5:
        if char.isalpha() or char == "-":
          text += char
    df.loc[i, "Column 6"] = text
  return df

# ตัวอย่างการใช้งาน
df = pd.read_excel("test.xlsx")
df = g(df)

df.to_excel('testfcolumn6.xlsx', index = False)