import pandas as pd
import numpy as np

import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve
import random

from sklearn.preprocessing import MinMaxScaler

import implicit


def final_func(file1):
    df = pd.read_csv(file1)
    # data_top  = df.head()
    id_list = list(df['CustomerID'].unique())
    return id_list


def info_func(file1, user_):
    li = []
    li2 = []
    di = {}
    df = pd.read_csv(file1)
    # data_top  = df.head()
    df=df[df['UnitPrice']> 0.0]
    id_list = list(df['CustomerID'].unique())
    print('user as ', user_)
    print("id list ", id_list)
    print("type ", type(user_))
    print('type df ', type(df['CustomerID'] ))
    df2=df[df['CustomerID'] == str(user_)]
    print('df2 ', df2)
    all_total = 0
    for index, row in df.iterrows():
        # print("roww ", row['CustomerID'])
        if str(row['CustomerID']) == user_:
            li.append(row['StockCode'])
            di['StockCode'] = row['StockCode']
            di['InvoiceDate'] = row['InvoiceDate']
            di['Description'] = row['Description'] 
            di['Quantity'] = row['Quantity']
            di['UnitPrice'] = row['UnitPrice']
            di['Total_Spending'] = round(row['Quantity'] * row['UnitPrice'],2)
            li2.append(di)
            di = {}
            # print("kitt")
            all_total = round(row['Quantity'] * row['UnitPrice'],2) + all_total
    # df2=df.query('CustomerID' == user_ )['Description']
    return li2,all_total



def grouped(file,user_):
    li = []
    di = {}
    print("user is ", user_)
    df = pd.read_csv(file)
    df.dropna(subset=['CustomerID'])
    df=df[df['UnitPrice']> 0.0]
    df['total_spend'] = df['Quantity'] * df['UnitPrice']
    # df.groupby('CustomerID')
    df1 = df.groupby(by='CustomerID').agg({'total_spend':'sum'}).reset_index()
    # print(df1)
    q = df1.quantile([0.00, 0.25, 0.50, 0.75, 1.00])
    q1 = df1[((df1['total_spend']>=q['total_spend'][0.00]) & (df1['total_spend']<q['total_spend'][0.50]))]
    q2 = df1[((df1['total_spend']>=q['total_spend'][0.50]) & (df1['total_spend']<q['total_spend'][0.75]))]
    q3 = df1[((df1['total_spend']>=q['total_spend'][0.75]) & (df1['total_spend']<=q['total_spend'][1.00]))]
    
    count = 0
    p_ = df.loc[df['CustomerID'] == float(user_)]['UnitPrice'].median()
    p_ = round(p_,2)
    cohort = 0
    for i in q1.loc[:,'CustomerID'] :
        if i == float(user_):
            f = 'The Customer is less spending so, '
            f = f + 'the recommended products should be around ', p_
            cohort = 1

            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < p_*1.5 and i > int(p_/1.5):
                    for j in li:
                        if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) == j['item']:
                            print("I is ", i)
                            break 
                    else:
                        di['item'] = (df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        di['price'] = df.loc[df['UnitPrice'] == i, 'UnitPrice'].head(1).to_string(index=False)
                        count = count + 1
                        li.append(di)
                        di = {}
                    
                if count == 5:
                    print(li)
                    break

            break

    for i in q2.loc[:,'CustomerID'] :
        if i == float(user_):
            cohort = 2

            f = 'The Customer is average spending so, '
            f = f + 'the recommended products should be around ', p_
            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < p_*1.5 and i > int(p_/1.5):
                    for j in li:
                        if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) == j['item']:
                            print("I is ", i)
                            break 
                    else:
                        di['item'] = (df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        di['price'] = (df.loc[df['UnitPrice'] == i, 'UnitPrice'].head(1).to_string(index=False))
                        count = count + 1
                        li.append(di)
                        di = {}
                    
                if count == 5:
                    break

            break
    for i in q3.loc[:,'CustomerID'] :
        if i == float(user_):
            cohort = 3
            f = 'The Customer is high spending so, '
            f = f + 'the recommended products shoulde be around ', p_
            count = 0
            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < p_*1.5 and i > int(p_/1.5):
                    for j in li:
                        if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) == j['item']:
                            print("I is ", i)
                            break 
                    else:
                        di['item'] = (df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        di['price'] = (df.loc[df['UnitPrice'] == i, 'UnitPrice'].head(1).to_string(index=False))
                        count = count + 1
                        li.append(di)
                        di = {}
                    
                if count == 5:
                    break

            break
    
    return f, li, cohort


def colab_rec(file,user_, p_):
    li = []
    di = {}
    print("user is ", user_)
    df = pd.read_csv(file)
    df.dropna(subset=['CustomerID'])
    df=df[df['UnitPrice']> 0.0]    
    df1 = df.loc[df['CustomerID'] == float(user_)]
    print(df1)
    df1['InvoiceDate']=pd.to_datetime(df1['InvoiceDate'])
    df2 = df1[df1['InvoiceDate']==df1['InvoiceDate'].max()]
    recent_item = df2.tail(1)
    print("rescent ",recent_item)
    recent_item_code = recent_item['StockCode'].head(1).to_string(index=False)
    print(recent_item_code)
    customer_item_matrix = df.pivot_table(
        index='CustomerID', 
        columns='StockCode', 
        values='Quantity',
        aggfunc='sum'
    )

    customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0)

    from sklearn.metrics.pairwise import cosine_similarity

    item_item_sim_matrix = pd.DataFrame(
        cosine_similarity(customer_item_matrix.T)
    )



    item_item_sim_matrix.columns = customer_item_matrix.T.index

    item_item_sim_matrix['StockCode'] = customer_item_matrix.T.index
    item_item_sim_matrix = item_item_sim_matrix.set_index('StockCode')


    top_10_similar_items = list(
    item_item_sim_matrix.loc[recent_item_code].sort_values(ascending=False).iloc[:10].index
    )
    # # print(top_10_similar_items)

    # df_f = df.loc[
    # df['StockCode'].isin(top_10_similar_items), 
    # ['StockCode', 'Description']
    # ].drop_duplicates().set_index('StockCode').loc[top_10_similar_items]
    # li = []
    # for i in df_f.itertuples():
    #     di['StockCode'] = getattr(i, 'Index')
    #     di['item'] = i[1]
    #     li.append(di)
    #     di = {}
    # # return li 

    df_f = df.loc[
    df['StockCode'].isin(top_10_similar_items), 
    ['StockCode', 'Description', "UnitPrice"]
    ].drop_duplicates().set_index('StockCode').loc[top_10_similar_items]
    if p_ == 3:
        df_f = df_f.groupby(['StockCode'], sort=False)['UnitPrice','Description'].max()
        li = []
        print(df_f)
        print("high")


    elif p_ == 1:

        df_f = df_f.groupby(['StockCode'], sort=False)['UnitPrice','Description'].min()
        li = []
        print(df_f)
        print("low")

    else:
        df_f1 = df_f.groupby(['StockCode'], sort=False)['UnitPrice'].median()
        df_f = pd.merge(df_f, df_f1, on='StockCode')
        print(df_f)
        df4 = df_f[~df_f.index.duplicated(keep='first')]
        print(df4)
        for i in df4.itertuples():
            
                di['StockCode'] = getattr(i, 'Index')
                di['item'] = i[1]
                di['UnitPrice'] = i[3]
                li.append(di)
                di ={}
        print("P is ", p_)
        return li

    for i in df_f.itertuples():
        di['StockCode'] = getattr(i, 'Index')
        di['UnitPrice'] = i[1]
        di['item'] = i[2]

        li.append(di)
        di = {}
    return li