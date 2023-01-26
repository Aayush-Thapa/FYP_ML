import pandas as pd
import numpy as np

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
            di['Description'] = row['Description'] 
            di['Quantity'] = row['Quantity']
            di['UnitPrice'] = row['UnitPrice']
            di['Total_Spending'] = round(row['Quantity'] * row['UnitPrice'],2)
            li2.append(di)
            di = {}
            print("kitt")
            all_total = round(row['Quantity'] * row['UnitPrice'],2) + all_total
    # df2=df.query('CustomerID' == user_ )['Description']
    return li2,all_total



def grouped(file,user_):
    li = []
    print("user is ", user_)
    df = pd.read_csv(file)
    df['total_spend'] = df['Quantity'] * df['UnitPrice']
    # df.groupby('CustomerID')
    df1 = df.groupby(by='CustomerID').agg({'total_spend':'sum'}).reset_index()
    # print(df1)
    q = df1.quantile([0.00, 0.25, 0.50, 0.75, 1.00])
    q1 = df1[((df1['total_spend']>=q['total_spend'][0.00]) & (df1['total_spend']<q['total_spend'][0.50]))]
    q2 = df1[((df1['total_spend']>=q['total_spend'][0.50]) & (df1['total_spend']<q['total_spend'][0.75]))]
    q3 = df1[((df1['total_spend']>=q['total_spend'][0.75]) & (df1['total_spend']<=q['total_spend'][1.00]))]
    
    df2 = df['UnitPrice'].unique()
    # q2 = df2.quantile([0.00, 0.25, 0.50, 0.75, 1.00])
    # print(q2)
    x = list(np.quantile(df2, np.arange( 0.25, 1, 0.25)))
    # print(x)
    for i in q1.loc[:,'CustomerID'] :
        if i == float(user_):
            f = 'less spending so, '
            f = f + 'recommended products should around than ', x[0]
        
            count = 0
            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < x[0]:
                    if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) in li:
                        print("I is ", i)
                        pass 
                    else:
                        li.append(df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        count = count + 1
                if count == 5:
                    break

            break

    for i in q2.loc[:,'CustomerID'] :
        if i == float(user_):
            f = 'average spending so, '
            f = f + 'recommended products should be around than ', x[0]
            count = 0
            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < x[1] and i > x[0]:
                    if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) in li:
                        print("I is ", i)
                        pass 
                    else:
                        li.append(df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        count = count + 1
                if count == 5:
                    break

            break
    for i in q3.loc[:,'CustomerID'] :
        if i == float(user_):
            f = 'high spending so, '
            f = f + 'recommended products around than ', x[0]
            count = 0
            for i in df.loc[:,'UnitPrice']:
                # print(i)
                if i < x[2] and i > x[1]:
                    if df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False) in li:
                        print("I is ", i)
                        pass 
                    else:
                        li.append(df.loc[df['UnitPrice'] == i, 'Description'].head(1).to_string(index=False))
                        count = count + 1
                    
                if count == 5:
                    break

            break
    
    return f, li

        
