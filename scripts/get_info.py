import pandas as pd

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
    # df2=df.query('CustomerID' == user_ )['Description']
    return li2