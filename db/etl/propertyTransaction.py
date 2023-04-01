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
    fetchTokenHeader = {
        'Content-Type': 'application/json',
        'AccessKey': URA_API_ACCESSKEY,
        'Accept': 'application/json',
        'User-Agent': 'PostmanRuntime/7.28.4'
    }  # returns html if i dont include user agent postman
    resp = requests.get(
        'https://www.ura.gov.sg/uraDataService/insertNewToken.action',
        headers=fetchTokenHeader)

    print(resp)
    print(resp.json())

    URA_API_TOKEN = resp.json()['Result']

    # Setting up default header for API calls
    apiHeader = {
        'Content-Type': 'application/json',
        'AccessKey': URA_API_ACCESSKEY,
        'Token': URA_API_TOKEN,
        'User-Agent': 'PostmanRuntime/7.30.1'
    }

    # Fetch data sets
    respPrivate1 = requests.get(
        'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1',
        headers=apiHeader)
    respPrivate2 = requests.get(
        'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=2',
        headers=apiHeader)
    respPrivate3 = requests.get(
        'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=3',
        headers=apiHeader)
    respPrivate4 = requests.get(
        'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=4',
        headers=apiHeader)
    respResale2017 = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3'
    )
    respResale2016 = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=1b702208-44bf-4829-b620-4615ee19b57c'
    )
    respResale2014 = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=83b2fc37-ce8c-4df4-968b-370fd818138b'
    )
    respResale2012 = requests.get(
        'https://data.gov.sg/api/action/datastore_search?resource_id=8c00bf08-9124-479e-aeca-7cc411d884c4'
    )

    private1 = respPrivate1.json()['Result']
    private2 = respPrivate2.json()['Result']
    private3 = respPrivate3.json()['Result']
    private4 = respPrivate4.json()['Result']
    resale2017 = respResale2017.json()["result"]["records"]
    resale2016 = respResale2016.json()["result"]["records"]
    resale2014 = respResale2014.json()["result"]["records"]
    resale2012 = respResale2012.json()["result"]["records"]

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

    # # Test query
    # testResult = db.query_find("main__PropertyTransactionsPrivate",
    #     { "y": "30589.1070785135" }
    # )

    # # Proof that query works
    # for x in testResult:
    #     print(x)

    # Query to get data - not super needed since currently fetching all, but just in case want to modify query
    resultPrivate = db.query_find("main__PropertyTransactionsPrivate", {})

    resultResale = db.query_find("main__PropertyTransactionsResale", {})

    transform(resultPrivate, resultResale)


# Transform data accordingly
def transform(resultPrivate, resultResale):

    print("Property Transaction: Transforming data")

    tempResale = list(resultResale)
    tempPrivate = list(resultPrivate)

    filteredResale = []
    tempPrivate2 = []

    for transaction in tempResale:
        if ('street_name'
                in transaction) and ('storey_range' in transaction) and (
                    'flat_type'
                    in transaction) and ('floor_area_sqm' in transaction) and (
                        'resale_price' in transaction) and (
                            'month' in transaction) and ('remaining_lease'
                                                         in transaction):
            filteredResale.append(transaction)

    # for result in tempPrivate:
    #     for transaction in result['transaction']:
    #         print

# removed block
# removed x y
# removed number of rooms
# changed date to varchar for now
# need map town to district
# tenure doing math
# executive flat types assume 3 BRs
# replacing enum for now

# Resale: Getting key/values we want
    for transaction in filteredResale:
        # tempBlock = transaction['block']
        # del transaction['block']

        transaction['district'] = 1  # need to map town to district
        transaction['street'] = transaction['street_name']
        # transaction['block'] = tempBlock # just for ordering for tuple down the road
        transaction['floorRangeStart'] = int(
            transaction['storey_range'].split(" ")[0])
        transaction['floorRangeEnd'] = int(
            transaction['storey_range'].split(" ")[2])
        transaction['propertyType'] = transaction['flat_type'] + "HDB"
        # transaction['noOfRoom'] = int(3 if transaction['flat_type'].split(" ")[0] == "EXECUTIVE" else transaction['flat_type'].split(" ")[0])
        transaction['area'] = float(transaction['floor_area_sqm'])
        transaction['price'] = float(transaction['resale_price'])
        transaction['transactionDate'] = transaction[
            'month']  # need to convert to date
        transaction['tenure'] = int(transaction['remaining_lease'].split(" ")
                                    [0])  # only taking year for now
        transaction['resale'] = True

        # To test centroids and district
        transaction['x'] = 10000.0000
        transaction['y'] = 10000.0000

        del transaction['block']
        del transaction['_id']
        del transaction['town']
        del transaction['street_name']
        del transaction['flat_type']
        del transaction['flat_model']
        del transaction['floor_area_sqm']
        del transaction['resale_price']
        del transaction['month']
        del transaction['remaining_lease']
        del transaction['lease_commence_date']
        del transaction['storey_range']

    print(tempResale[0])

    for result in tempPrivate:
        for transaction in result['transaction']:

            # for reordering
            tempType = transaction['propertyType']
            del transaction['propertyType']
            tempArea = transaction['area']
            del transaction['area']
            tempPrice = transaction['price']
            del transaction['price']
            tempTenure = transaction['tenure']
            del transaction['tenure']

            # logic to manage B levels in floor range
            if (transaction['floorRange'].split("-")[0] == ""):
                floorRangeStart = 0
                floorRangeEnd = 0
            else:
                if ("B" in transaction['floorRange'].split("-")[0]):
                    floorRangeStart = -int(
                        transaction['floorRange'].split("-")[0][1:])
                else:
                    floorRangeStart = int(
                        transaction['floorRange'].split("-")[0])

                if ("B" in transaction['floorRange'].split("-")[1]):
                    floorRangeEnd = -int(
                        transaction['floorRange'].split("-")[1][1:])
                else:
                    floorRangeEnd = int(
                        transaction['floorRange'].split("-")[1])

            transaction['district'] = int(transaction['district'])
            transaction['street'] = result['street']
            transaction['floorRangeStart'] = floorRangeStart
            transaction['floorRangeEnd'] = floorRangeEnd
            transaction['propertyType'] = tempType
            transaction['area'] = float(tempArea)
            transaction['price'] = float(tempPrice)
            transaction['transactionDate'] = transaction['contractDate']
            transaction['tenure'] = int(1000000 if tempTenure == "Freehold"
                                        else 10)  # ill do the math later
            transaction['resale'] = False

            # To test centroids and district
            transaction['x'] = 10000.0000
            transaction['y'] = 10000.0000

            del transaction['noOfUnits']
            del transaction['contractDate']
            del transaction['typeOfSale']
            del transaction['typeOfArea']
            del transaction['floorRange']

            tempPrivate2.append(transaction)

    print(tempPrivate2[0])

    filteredPrivate = []

    for transaction in tempPrivate2:
        if ('street_name'
                in transaction) and ('storey_range' in transaction) and (
                    'flat_type'
                    in transaction) and ('floor_area_sqm' in transaction) and (
                        'resale_price' in transaction) and (
                            'month' in transaction) and ('remaining_lease'
                                                         in transaction):
            filteredPrivate.append(transaction)

    combinedTransactions = filteredResale + filteredPrivate

    print(combinedTransactions[0])

    load(combinedTransactions)


# Load data into MySQL accordingly
def load(result):

    print("Property Transaction: Loading data")

    # Transform data to list of values
    result = list(map(lambda x: tuple(x.values()), result))

    print(result[0])

    # Insert data
    db = DataWarehouse(True, False)
    db.insert_to_schema("main__PropertyTransaction", result)


extract()
