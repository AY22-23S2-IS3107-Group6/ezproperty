import pymongo
import pandas as pd
import datetime
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
    filteredPrivateProjects = []
    filteredPrivateTransactions = []


    for transaction in tempResale:
        if ('street_name' in transaction) and ('storey_range' in transaction) and ('flat_type' in transaction) and ('floor_area_sqm' in transaction) and ('resale_price' in transaction) and ('month' in transaction) and ('remaining_lease' in transaction):
            filteredResale.append(transaction)

# removed block
# removed x y
# removed number of rooms
# executive flat types assume 3 BRs
# replacing enum for now

# TO DO
# Insert all data properly (insert into one schema + fetch more records)
# tenure doing math

# need map town to district

    # Resale: Getting key/values we want
    for transaction in filteredResale:

        transaction['district'] = 1
        transaction['street'] = transaction['street_name']
        transaction['floorRangeStart'] = int(transaction['storey_range'].split(" ")[0])
        transaction['floorRangeEnd'] = int(transaction['storey_range'].split(" ")[2])
        transaction['propertyType'] = transaction['flat_type'] + "HDB"
        transaction['area'] = float(transaction['floor_area_sqm'])
        transaction['price'] = float(transaction['resale_price']) 

        # Convert date to SQL formatting
        year = int(transaction['month'].split("-")[0])
        month = int(transaction['month'].split("-")[1])
        date = datetime.datetime(year, month, 1)
        dateSql = date.strftime('%Y-%m-%d')

        transaction['transactionDate'] = dateSql
        transaction['tenure'] = int(transaction['remaining_lease'].split(" ")[0]) # only taking year for now
        transaction['resale'] = True

        # Code for no of room if want to add in 
        # transaction['noOfRoom'] = int(3 if transaction['flat_type'].split(" ")[0] == "EXECUTIVE" else transaction['flat_type'].split(" ")[0])

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


    for project in tempPrivate:
        checker = True
        for transaction in project['transaction']:
            if ('propertyType' not in transaction) or ('area' not in transaction) or ('price' not in transaction) or ('tenure' not in transaction) or ('floorRange' not in transaction) or ('district' not in transaction) or ('contractDate' not in transaction):
                checker = False
        
        if ('street' not in project):
            checker = False

        if checker:
            filteredPrivateProjects.append(project)

    for project in filteredPrivateProjects:
        for transaction in project['transaction']:

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
                    floorRangeStart = -int(transaction['floorRange'].split("-")[0][1:])
                else:
                    floorRangeStart = int(transaction['floorRange'].split("-")[0])
                
                if ("B" in transaction['floorRange'].split("-")[1]):
                    floorRangeEnd = -int(transaction['floorRange'].split("-")[1][1:])
                else:
                    floorRangeEnd = int(transaction['floorRange'].split("-")[1])
                    

            transaction['district'] = int(transaction['district'])
            transaction['street'] = project['street']
            transaction['floorRangeStart'] = floorRangeStart
            transaction['floorRangeEnd'] = floorRangeEnd
            transaction['propertyType'] = tempType
            transaction['area'] = float(tempArea)
            transaction['price'] = float(tempPrice)

            # Convert date to SQL formatting
            year = int("20" + transaction['contractDate'][-2:])
            month = int(transaction['contractDate'][:2])
            date = datetime.datetime(year, month, 1)
            dateSql = date.strftime('%Y-%m-%d')

            transaction['transactionDate'] = dateSql
            transaction['tenure'] = int(1000000 if tempTenure == "Freehold" else 10) # ill do the math later
            transaction['resale'] = False

            if ('nettPrice' in transaction):
                del transaction['nettPrice']
            del transaction['noOfUnits']
            del transaction['contractDate']
            del transaction['typeOfSale']
            del transaction['typeOfArea']
            del transaction['floorRange']

            filteredPrivateTransactions.append(transaction)

    print(filteredPrivateTransactions[0])

    combinedTransactions = filteredPrivateTransactions + filteredResale

    print(filteredPrivateTransactions[0])
    print(filteredResale[0])

    # filteredCombinedTransactions = []

    # for transaction in combinedTransactions:
    #     if ('district' in transaction) and ('street' in transaction) and ('floorRangeStart' in transaction) and ('floorRangeEnd' in transaction) and ('propertyType' in transaction) and ('area' in transaction) and ('price' in transaction) and ('transactionDate' in transaction) and ('tenure' in transaction) and ('resale' in transaction):
    #         filteredCombinedTransactions.append(transaction)

    # print("Pre filter length", len(combinedTransactions))
    # print("Post filter length", len(filteredCombinedTransactions))
    
    print(combinedTransactions[0])

    load(combinedTransactions)


# Load data into MySQL accordingly
def load(result):

    print("Property Transaction: Loading data")

    # Transform data to list of values
    result = list(map(lambda x: tuple(x.values()), result))

    for temp in result:
        if len(temp) != 10:
            print("FAILING", temp)

    print(result[0])
    print(result[101])


    # Insert data
    db = DataWarehouse(True, False)
    db.insert_to_schema("main__PropertyTransaction", result)


extract()


