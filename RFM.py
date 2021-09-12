##### RFM İLE MÜŞTERİ SEGMENTASYONU #####


import pandas as pd
import datetime as dt

# recency değeri için tarih belirleme
today_date = dt.datetime(2011,12,11)

# Tüm sütunları göster
pd.set_option('display.max_columns',None)

# Tüm satırları göster
pd.set_option('display.max_rows',None)

# Virgülden sonra 5 basamak göster
pd.set_option('display.float_format',lambda x:'%.5f' %x)

df_copy = pd.read_excel("online_retail_II.xlsx",sheet_name="Year 2010-2011")

df = df_copy.copy()

# Veriyi anlamak için gerekenleri yazdırır.
"""
def dataframe_info(df):

    print("-----Head-----","\n",df.head())

    print("\n-----Tail-----","\n",df.tail())

    print("\n-----Shape-----","\n",df.shape)

    print("\n-----Info-----","\n",df.info)

    print("\n-----Columns-----","\n",df.columns)

    print("\n-----Index-----","\n",df.index)

    print("\n-----Statistical Values-----","\n",df.describe().T)

dataframe_info(df)

print("\n")
"""

# Eksik gözlem içeren değişkenler

print(df.isnull().any())

print("\n")


# Değişkenlerin içerdiği eksik gözlem miktarı

print(df.isnull().sum())

print("\n")

# Eksik gözlemleri veriden çıkarma

df.dropna(inplace = True)

print("----- Eksik gözlemler çıkarıldıktan sonra veri seti ------\n",df.head())

print("\n")

# Eşsiz ürün sayısı

print(df['StockCode'].nunique())

print("\n")

# Ürünlerin kategorilerine göre sayısı

print(df['StockCode'].value_counts())

print("\n")

# En çok sipariş edilen 5 ürünün çoktan aza doğru sıralanması

print(df['StockCode'].value_counts().sort_values(ascending=False).head(5))

print("\n")

# İptal edilen işlemleri veriden çıkartma

df = df[~df['Invoice'].str.contains('C',na=False)]

df = df[(df['Quantity'] > 0)]

df = df[(df['Price'] > 0)]

# Fatura başına elde edilen toplam kazanç

df['TotalPrice'] = df['Quantity'] * df['Price']

print(df.head())

print("\n")
# RFM Metriklerinin Hesaplanması

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice':lambda Invoice:Invoice.nunique(),
                                     'TotalPrice':lambda TotalPrice:TotalPrice.sum()})


rfm.columns = ['recency','frequency','monetary']

rfm = rfm[(rfm['monetary'] > 0)]

print("-------- RFM --------\n",rfm.head())

####### RFM SKORLARININ OLUŞTURULMASI #######
print("\n")
# Recency

rfm['recency_score'] = pd.qcut(rfm['recency'],5,labels = [5,4,3,2,1])

# Frequency

rfm['frequency_score'] = pd.qcut(rfm['frequency'].rank(method="first"),5,labels = [1,2,3,4,5])

# Monetary

rfm['monetary_score'] = pd.qcut(rfm['monetary'],5,labels = [1,2,3,4,5])

# RFM SKORLARININ TEK BİR DEĞİŞKENE ÇEVRİLMESİ #

rfm['RFM_SCORE'] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))

##### RFM SKORLARININ SEGMENT OLARAK TANIMLANMASI ####

seg_map = {r'[1-2][1-2]':'hibernating',
           r'[1-2][3-4]':'at_risk',
           r'[1-2]5':'can\'t_loose',
           r'3[1-2]':'about_to_sleep',
           r'33':'need_attention',
           r'[3-4][4-5]':'loyal_customers',
           r'41':'promising',
           r'51':'new_customers',
           r'[4-5][2-3]':'potential_loyalists',
           r'5[4-5]':'champions',
           }

rfm['SEGMENT'] = rfm['RFM_SCORE'].replace(seg_map,regex = True)

print("\n")

print(" --------- SEGMENTLER --------- \n")

print(rfm['SEGMENT'].head(10))

print("\n")
print('new_customers segmentinin istatistiksel değerleri')
print("\n")
print(rfm[rfm['SEGMENT']=='new_customers'].describe().T)
print("\n")
print('need_attention segmentinin istatistiksel değerleri')
print("\n")
print(rfm[rfm['SEGMENT']=='need_attention'].describe().T)
print("\n")
print('can\'t_loose segmentinin istatistiksel değerleri')
print("\n")
print(rfm[rfm['SEGMENT']=='can\'t_loose'].describe().T)
print("\n")

##### SEGMENT, RECENCY, FREQUENCY, MONETARY KIRILIMINDA BETİMSEL İSTATİSTİKLER #####

print(rfm[['SEGMENT','recency','frequency','monetary']].groupby('SEGMENT').agg(['mean','count']))

