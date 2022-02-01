#!/usr/bin/env python
# coding: utf-8

# # モバイル空間統計データから、あるメッシュの滞在数の時系列をファイルに保存するコード
ライブラリのインポート
# In[1]:


import jismesh.utils as ju
# コントロールパネルで Anaconda prompt を検索.
# jismeshはanaconda promptでpip install jismeshでインストールできる
import csv
import pandas as pd
import numpy as np
import glob
import matplotlib as mpl
import matplotlib.pyplot as plt

ファイルの読み込み。ファイル名やフォルダ位置などは適宜変更のこと。
df_sesndaiStation = ...の部分で、読み込むメッシュ番号を指定している。
# In[44]:


list = glob.glob('C:/Users/ryo itoh/Desktop/DIM new/unzip/1000/*00000.csv')

#df_Koku_Series = pd.DataFrame(columns=['date','time','area','residence','age','gender','population'])
#df_Kyodai_Series = pd.DataFrame(columns=['date','time','area','residence','age','gender','population'])
#df_Todai_Series = pd.DataFrame(columns=['date','time','area','residence','age','gender','population'])
#df_Kawauchi_Series = pd.DataFrame(columns=['date','time','area','residence','age','gender','population'])
df_SendaiStation_Series = pd.DataFrame(columns=['date','time','area','residence','age','gender','population'])

#del df
#del df_Koku

for file in list:
    infile = file
    df = pd.read_csv(infile,header=0)
    df_SendaiStation = df[df.area==574037101]
    df_SendaiStation_Series = df_SendaiStation_Series.append(df_SendaiStation)
    print(file)

    
#df_Koku_Series.sort_values('date')
#print(df_Koku_Series)
#df_Todai_Series.sort_values('date')
#print(df_Todai_Series)
#df_Koku_Series.sort_values('date')
#dataの型を数値列から日付に変更しています。
df_SendaiStation_Series['date'] = pd.to_datetime(df_SendaiStation_Series['date'].astype(str))
df_SendaiStation_Series.sort_values('date')
print(df_SendaiStation_Series)


# In[48]:


# データをプロットする。
pd.to_datetime(df_SendaiStation_Series["date"].astype(str))                      #データの型を日付に変える
plt.plot(df_SendaiStation_Series['date'], df_SendaiStation_Series['population']) # 折れ線グラフをプロット

plt.title('Mobility Change at Sendai station')          # 図のタイトル
plt.xlabel('date')                    # x軸のラベル
plt.xticks(rotation=90)               #x軸を縦書きに変える
plt.ylabel('Population')              # y軸のラベル

plt.savefig("Mobility at Sendai station.png")
plt.show()

出力ファイルを指定
# In[11]:


outfile = 'D:/unzip/SendaiStation_Series574037101_2019-2021.csv'
df_SendaiStation_Series.to_csv(outfile)

