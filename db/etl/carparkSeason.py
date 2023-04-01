import pymongo
import pandas as pd
import requests
from ..lake import DataLake
from ..warehouse import DataWarehouse


# Feed data into lake / mongoDB
def extract():

    print("Carpark Season: Feeding data into lake")

    URA_API_ACCESSKEY = '84d7c27b-8dc6-4a34-9ea3-7769c174007c'

    # Fetches daily token which is needed along with access key for API calls
    fetchTokenHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Accept': 'application/json', 'User-Agent': 'PostmanRuntime/7.28.4'} # returns html if i dont include user agent postman
    resp = requests.get('https://www.ura.gov.sg/uraDataService/insertNewToken.action', headers = fetchTokenHeader) 

    print(resp)
    print(resp.json())

    URA_API_TOKEN = resp.json()['Result']

    # Setting up default header for API calls
    apiHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Token': URA_API_TOKEN, 'User-Agent': 'PostmanRuntime/7.30.1'}

    # Fetch both data sets
    respSeason = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Season_Car_Park_Details', headers = apiHeader)

    carparkSeason = respSeason.json()['Result']

    # Insert data
    db = DataLake()
    db.insert_to_schema("amn__CarparkSeason", carparkSeason) # no logic currently to manage reloading data, so uncomment this after populating db

    # Test query
    testResult = db.query_find("amn__CarparkSeason", 
        { "ppCode": "GA002" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    # Query to get data - not super needed since currently fetching all, but just in case want to modify query
    result = db.query_find("amn__CarparkSeason", 
        {}
    )
    
    transform(result)


# Transform data accordingly
def transform(result):
   
    print("Carpark Season: Transforming data")

    temp = list(result)
    filteredCarparks = []

    # Remove carparks with missing data
    for carpark in temp:
        if ('ppCode' in carpark) and ('ppName' in carpark) and ('vehCat' in carpark) and ('monthlyRate' in carpark) and ('parkingHrs' in carpark) and ('ticketType' in carpark):
            if carpark['geometries'] != []:
                filteredCarparks.append(carpark)


    # Flatten coordinates
    # Bring out into x and y key
    for carpark in filteredCarparks:
        carpark['x'] = float(carpark['geometries'][0]['coordinates'].split(",")[0])
        carpark['y'] = float(carpark['geometries'][0]['coordinates'].split(",")[1])
        carpark['_id'] = id(carpark['_id']) # using python generated _id for now since cant find a suitable pkey
        del carpark['geometries']
        # del carpark['_id'] # uncomment this code if we decide we don't need _id if we using our own pkeys

    # Typecast appropriately to feed into sql
    for carpark in filteredCarparks:
        carpark['monthlyRate'] = int(carpark['monthlyRate'])

    print(filteredCarparks[0])

    load(filteredCarparks)


# Load data into MySQL accordingly
def load(result):

    print("Carpark Season: Loading data")

    # Transform data to list of values
    result = list(map(lambda x: tuple(x.values()), result))

    # Insert data
    db = DataWarehouse()
    db.insert_to_schema("amn__CarparkSeason", result)


extract()


