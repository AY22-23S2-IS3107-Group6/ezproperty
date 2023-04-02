import pymongo
import pandas as pd
import requests
from bs4 import BeautifulSoup
from decimal import Decimal

from ..lake import DataLake
from ..warehouse import DataWarehouse

def extract():
    # make a request to the site and get it as a string
    markup = requests.get(f'https://github.com/hxchua/datadoubleconfirm/blob/master/datasets/mrtsg.csv').text

    # pass the string to a BeatifulSoup object
    soup = BeautifulSoup(markup, 'html.parser')

    # web scraping
    table = soup.find('table', class_='js-csv-data csv-data js-file-line-container')

    df = pd.DataFrame(columns=['id', 'stationName', 'stationNo', 'x', 'y', 'latitude', 'longitude', 'colour'])

    for row in table.tbody.find_all('tr'):
        # find all data for each column
        columns = row.find_all('td')

        if (columns != []):
            id = columns[1].text.strip()
            stationName = columns[2].text.strip()
            stationNo = columns[3].text.strip()
            x = columns[4].text.strip()
            y = columns[5].text.strip()
            latitude = columns[6].text.strip()
            longitude = columns[7].text.strip()
            colour = columns[8].text.strip()

            df = pd.concat([df, pd.DataFrame.from_records([{
                'id': id,
                'stationName': stationName,
                'stationNo': stationNo,
                'x': x,
                'y': y,
                'latitude': latitude,
                'longitude': longitude,
                'colour': colour,
            }])])
    
    # check data
    print("Check web scraped data")
    print(df.head())

    db = DataLake()
    # db.insert_to_schema("amn__TrainStation", df.to_dict('records'))

    testResult = db.query_find("amn__TrainStation", 
        { "stationNo": "EW5" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    result = db.query_find("amn__TrainStation", 
        {}
    )
    
    transform(result)


def transform(result):
    result = list(result)

    # Transform data accordingly
    print("Test: Transforming data")
    for trainStation in result:
        trainStation['x'] = Decimal(trainStation['x'])
        trainStation['y'] = Decimal(trainStation['y'])
        trainStation['latitude'] = Decimal(trainStation['latitude'])
        trainStation['longitude'] = Decimal(trainStation['longitude'])
        trainStation['_id'] = id(trainStation['_id']) # using python generated _id for now since cant find a suitable pkey
        del trainStation['id']

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")
    print(result[0])

    result = list(map(lambda x: tuple(x.values()), result))
    # result = result.map(lambda x: tuple(x.values()))
    
    # Insert data
    db = DataWarehouse(True,True)
    db.insert_to_schema("amn__TrainStation", result)

    # Query data using SQL
    # result = db.query('''
    #     SELECT * FROM amn__TrainStation
    # ''')

    # for x in result:
    #     print(x)


extract()