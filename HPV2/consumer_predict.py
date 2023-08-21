import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')
from kafka import KafkaConsumer

lr = pickle.load(open('model.pkl', 'rb'))

kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'my_topic'  # Replace with your Kafka topic

consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_bootstrap_servers)

df = pd.read_csv('test.csv')

# Consume messages from Kafka and collect data for model fitting
for message in consumer:
    data = message.value.decode()
    data = data.split(',')
    x = data
    x = np.array(x).reshape(1, -1)
            
    x = pd.DataFrame(x, columns=df.columns)
    # print(x)
    
    data = x
    # data = pd.DataFrame(data).T
    column_list = ['OverallQual', 'GrLivArea', 'GarageCars', 'GarageArea', 'TotalBsmtSF',
        '1stFlrSF', 'FullBath', 'TotRmsAbvGrd', 'YearBuilt', 'YearRemodAdd',
        'MasVnrArea', 'Fireplaces', 'GarageYrBlt', 'BsmtFinSF1', 'LotFrontage',
        'WoodDeckSF', '2ndFlrSF', 'OpenPorchSF', 'HalfBath', 'LotArea',
        'BsmtFullBath', 'BsmtUnfSF', 'BedroomAbvGr', 'ScreenPorch']
    data = data[column_list]
    # data.fillna(df.median(), inplace=True)
    data.fillna(df.mode().iloc[0], inplace=True)
    data.replace('NA', df.mode().iloc[0], inplace=True)
    # data = pd.DataFrame(SS.transform(data), columns=data.columns)
    pred = lr.predict(data)
    data['SalePrice'] = pred
    
    print(data)