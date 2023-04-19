# %%
# Provided: notebook bootstrapping
# Keras Models
import tensorflow as tf
import keras 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, BatchNormalization, Conv2D, MaxPooling2D

# Aditional Libs
import numpy as np
import os
import pandas as pd
import pickle
import time


import sys
module_path = os.path.abspath(os.path.join('..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path) 

from db.warehouse import DataWarehouse

module_path = os.path.abspath(os.path.join('../..'))
print(module_path)
if module_path not in sys.path:
    sys.path.append(module_path) 
from db.etl import MultilayerPerceptronPipeline

pipe = MultilayerPerceptronPipeline()
schema_name = 'ml__MultiLayerPerceptron'



# Creates a new MLP and loads into datalake
def update_model():
    db = DataWarehouse()

    dataset = db.query('''
        SELECT district, floorRangeStart, floorRangeEnd, area, transactionDate, resale, price FROM main__PropertyTransaction
        LIMIT 5000
    ''')

    # Data pre-processing to convert all to float and standardise magnitude
    df = pd.DataFrame(dataset)
    for column in df.columns:
        if column == "transactionDate":
            df[column] = pd.to_datetime(df[column])
            df[column] = (df[column].max() - df[column]) / np.timedelta64(1,'Y')
        if column == "price": # price is in millions
            df[column] = df[column].astype(float) / 1e6
        if column == "area": # area is in 100 square metre
            df[column] = df[column].astype(float) / 100
        else:
            df[column] = df[column].astype(float)
    print(df.tail())
    print(df.dtypes)


    # Splitting data into train and test
    train = df.sample(frac=0.9,random_state=200)
    test = df.drop(train.index)

    X_train, Y_train = train[[column for column in df.columns if column != 'price']], train['price']
    X_test, Y_test = test[[column for column in df.columns if column != 'price']], test['price']

    print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)

    # Building model with 3 hidden layers, each with 64 neurons
    mlp_model = keras.Sequential()
    mlp_model.add(Dense(6, activation='relu', input_shape=(6,)))
    mlp_model.add(Dense(64, activation='relu'))
    mlp_model.add(Dense(64, activation='relu'))
    mlp_model.add(Dense(64, activation='relu'))
    mlp_model.add(Dense(1, activation='linear'))

    # Compile the model
    mlp_model.compile(optimizer= tf.keras.optimizers.Adam(learning_rate=0.001), loss='mae', metrics=['mae'])

    # Train model
    mlp_history = mlp_model.fit(X_train, Y_train, epochs=10, batch_size=16)

    # Check accuracy and error
    loss, acc = mlp_model.evaluate(X_test, Y_test)
    print(X_test.shape)
    print(f'test loss is {loss}')
    print(f'test accuracy is {acc}')

    # remove previous model
    pipe.dl_delete_all(schema_name)

    #pickling the model
    pickled_model = pickle.dumps(mlp_model)
    
    # creating other attributes
    model = [{ "model": pickled_model, 'name': "MLP", 'created_time': time.time()}]
    pipe.dl_loader(model, schema_name)



# Retrieves MLP from Data Lake and predicts price 
def load_from_db_and_predict(district, floorRangeStart, floorRangeEnd, area, transactionDate, resale):

    result = pipe.dl_getter('ml__MultiLayerPerceptron')
    model = pickle.loads(result[0]["model"])
    print(model)

    input_data  = np.array([[district, floorRangeStart, floorRangeEnd, area, transactionDate, resale]])
    pred_price = model.predict(input_data)
    print(pred_price)

    return pred_price

    # load_from_db_and_predict(3.0, 6.0, 10.0, 1.06, 1.579772, 0.0)    


# %%



