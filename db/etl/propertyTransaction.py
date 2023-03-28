import pymongo
import pandas as pd
import requests
from ..lake import DataLake
from ..warehouse import DataWarehouse


# Feed data into lake / mongoDB
def extract():

    print("Property Transaction: Feeding data into lake")

    URA_API_ACCESSKEY = '84d7c27b-8dc6-4a34-9ea3-7769c174007c'

    # Fetches daily token which is needed along with access key for API calls
    fetchTokenHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Accept': 'application/json', 'User-Agent': 'PostmanRuntime/7.28.4'} # returns html if i dont include user agent postman
    resp = requests.get('https://www.ura.gov.sg/uraDataService/insertNewToken.action', headers = fetchTokenHeader) 

    print(resp)
    print(resp.json())

    URA_API_TOKEN = resp.json()['Result']

    # Setting up default header for API calls
    apiHeader = {'Content-Type': 'application/json', 'AccessKey': URA_API_ACCESSKEY, 'Token': URA_API_TOKEN, 'User-Agent': 'PostmanRuntime/7.30.1'}

    # Fetch data sets
    respPrivate1 = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1', headers = apiHeader)
    respPrivate2 = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=2', headers = apiHeader)
    respPrivate3 = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=3', headers = apiHeader)
    respPrivate4 = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=4', headers = apiHeader)
    respResale2017 = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3')
    respResale2016 = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=1b702208-44bf-4829-b620-4615ee19b57c')
    respResale2014 = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=83b2fc37-ce8c-4df4-968b-370fd818138b')
    respResale2012 = requests.get('https://data.gov.sg/api/action/datastore_search?resource_id=8c00bf08-9124-479e-aeca-7cc411d884c4')


    private1 = respPrivate1.json()['Result']
    private2 = respPrivate2.json()['Result']
    private3 = respPrivate3.json()['Result']
    private4 = respPrivate4.json()['Result']
    resale2017 = respResale2017.json()["result"]["records"]
    resale2016 = respResale2016.json()["result"]["records"]
    resale2014 = respResale2014.json()["result"]["records"]
    resale2012 = respResale2012.json()["result"]["records"]

    # print("Private1",private1[0])
    # print("Private2",private2[0])
    # print("Private3",private3[0])
    # print("Private4",private4[0])

    # print("Resale2017",resale2017[0])
    # print("Resale2016",resale2016[0])
    # print("Resale2014",resale2014[0])
    # print("Resale2012",resale2012[0])


    # Insert data
    db = DataLake()
    print("FIRST ONE")
    db.insert_to_schema("main__PropertyTransactionsPrivate", private1)
    print("SECOND ONE")
    db.insert_to_schema("main__PropertyTransactionsPrivate", private2)
    print("THIRD ONE")
    db.insert_to_schema("main__PropertyTransactionsPrivate", private3)
    print("FOURTH ONE")
    db.insert_to_schema("main__PropertyTransactionsPrivate", private4)
    print("FIFTH ONE")
    db.insert_to_schema("main__PropertyTransactionsResale", resale2017)
    # print("SIX ONE") - bug not inserting more than one schema in
    # db.insert_to_schema("main__PropertyTransactionsResale", resale2016)
    # print("SEVEN ONE")
    # db.insert_to_schema("main__PropertyTransactionsResale", resale2014)
    # print("EIGHT ONE")
    # db.insert_to_schema("main__PropertyTransactionsResale", resale2012)


    # Test query
    testResult = db.query_find("main__PropertyTransactionsPrivate", 
        { "y": "30589.1070785135" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    # Query to get data - not super needed since currently fetching all, but just in case want to modify query
    resultPrivate = db.query_find("main__PropertyTransactionsPrivate", 
        {}
    )

    resultResale = db.query_find("main__PropertyTransactionsResale", 
        {}
    )
    
    transform(resultPrivate, resultResale)


# Transform data accordingly
def transform(resultPrivate, resultResale):
   
    print("Property Transaction: Transforming data")

    tempResale = list(resultResale)
    tempPrivate = list(resultPrivate)

    filteredResale = []
    filteredPrivate = []

    # Resale: Getting key/values we want
    for transaction in filteredResale:
        # need to map town to district
        transaction['street'] = transaction['street_name']
        transaction['floorRangeStart'] = int(transaction['storey_range'].split(" ")[0])
        transaction['floorRangeEnd'] = int(transaction['storey_range'].split(" ")[2])
        transaction['propertyType'] = transaction['flat_type'] + "HDB"
        transaction['noOfRoom'] = int(transaction['flat_type'].split(" ")[0])
        transaction['area'] = transaction['floor_area_sqm']
        transaction['price'] = transaction['resale_price']
        transaction['transactionDate'] = transaction['month'] # need to convert to date
        transaction['tenure'] = transaction['remaining_lease']
        transaction['resale'] = True

        del transaction['street_name']
        del transaction['flat_type']
        del transaction['flat_model']
        del transaction['floor_area_sqm']
        del transaction['street_name']
        del transaction['resale_price']
        del transaction['month']
        del transaction['remaining_lease']
        del transaction['lease_commence_date']
        del transaction['storey_range']

    # Typecast appropriately to feed into sql
    for carpark in filteredCarparks:
        carpark['monthlyRate'] = int(carpark['monthlyRate'])

    print(filteredCarparks[0])

    load(filteredCarparks)


# Load data into MySQL accordingly
def load(result):

    print("Property Transaction: Loading data")

    # # Transform data to list of values
    # result = list(map(lambda x: tuple(x.values()), result))

    # # Insert data
    # db = DataWarehouse()
    # db.insert_to_schema("amn__CarparkSeason", result)


extract()


