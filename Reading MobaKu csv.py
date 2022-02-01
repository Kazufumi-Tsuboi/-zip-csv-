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
#outfile = 'D:/unzip/Koku_Series574036194.csv'
#df_Koku_Series.to_csv(outfile)
#outfile = 'D:/unzip/Todai_Komaba_Series533935942_age15_gender1.csv'
#df_Todai_Series.to_csv(outfile)
#outfile = 'D:/unzip/Tohoku_Kawauchi_Series574036181_age15_gender1_time1000.csv'
df_SendaiStation_Series.to_csv(outfile)

（以下は3次メッシュでの集計用です。無視してください）特定の市区町村が居住地である行のみを抽出
町田市　13209
習志野市　12216
仙台市青葉区　04101
仙台市宮城野区　04102
市区町村コードは　https://www.soumu.go.jp/denshijiti/code.html　などを参照。
最初の桁が0である場合、無視される（変数を整数として読み込んでいるため）。現状では問題は確認されていないが、留意しておく。
# In[ ]:


df_Aoba = df[(df.residence==4101)]
df_Aoba

滞在者数を3次メッシュ（約1km四方）ごとに集計。元データでは集計単位は1/2地域メッシュ（1辺約500m）となっている。
500mメッシュコードの下一桁は0-3の値をとり、この4つのメッシュをまとめたものが3次メッシュと等しい。
agg_Aobaの計算では、df_Aoba.area（に1を足したもの）を10で割った整数部を取って3次メッシュ値を計算し、3次メッシュ値が等しいセルはgroupbyでグループとし、それをagg('sum')で足し合わせている。area以外の列も足し算されてしまうが、今後利用しない。
as_index=Trueで、グルーピングに使った値（＝3次メッシュの値）をagg_Aobaのインデックスとして使うことにしている。

下2行はチェック用で、実際にいくつかのメッシュで集計がうまくできていることを直接確認できる。3次メッシュ53393750に対応する1/2メッシュは、533937500-53393753だが、上の行でdf_Aobaの対応する行を表示し、populationの合計が、agg_Aobaのそれと等しいことが見える。
# In[ ]:


agg_Aoba = df_Aoba.groupby( (df_Aoba.area) // 10, as_index=True).agg('sum')
agg_Aoba

#print(df_Aoba[(df_Aoba.area>533937500)&(df_Aoba.area<533937510)])
#print(agg_Aoba[agg_Aoba.index==53393750])

集計値とインデックスを一つの変数としてまとめる。
# In[ ]:


agg_out = [agg_Aoba.index.T,agg_Aoba.population.T]
agg_out

agg_outをファイルに保存。
# In[ ]:


outfile = infile.replace('../data/','../results/Aoba')
np.savetxt(outfile,np.transpose(agg_out),delimiter=',',fmt='%d')

