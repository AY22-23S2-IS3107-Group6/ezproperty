import pymongo
import pandas as pd
import requests
from ..lake import DataLake
from ..warehouse import DataWarehouse


# Feed data into lake / mongoDB
def extract():

    print("Rental Transactions: Feeding data into lake")

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
    resp = requests.get('https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Rental_Median', headers = apiHeader)

    rentalTransactions = resp.json()['Result']

    # Insert data
    db = DataLake()
    db.insert_to_schema("main__RentalPropertyMedian", rentalTransactions) # no logic currently to manage reloading data, so uncomment this after populating db

    # Test query
    testResult = db.query_find("main__RentalPropertyMedian", 
        { "project": "ELLIOT AT THE EAST COAST" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    # Query to get data - not super needed since currently fetching all, but just in case want to modify query
    result = db.query_find("main__RentalPropertyMedian", 
        {}
    )
    
    transform(result)


# Transform data accordingly
def transform(result):
   
    print("Rental Transactions: Transforming data")

    temp = list(result)
    rentalProject = []

    # Remove projects with missing data
    for project in temp:
        if ('rentalMedian' in project) and ('street' in project) and ('x' in project) and ('project' in project) and ('y' in project):
            if project['rentalMedian'] != []:
                rentalProject.append(project)

    # Typecast appropriately to feed into sql
    for project in rentalProject:
        project['x'] = float(project['x'])
        project['y'] = float(project['y'])

    rentalMedian = []

    # Break into two tables
    for project in rentalProject:

        # this will be used as the rental project ID
        project['_id'] = id(project['_id']) # using python generated _id for now since cant find a suitable pkey

        tempMedians = project['rentalMedian']

        # Bring out all the rental medians (flatten) into a new json object
        for median in tempMedians:
            rentalMedian.append(median)
            # add foreign key linking to project
            median['rentalProject'] = project['_id']

        del project['rentalMedian']

    print(rentalProject[0])
    print(rentalMedian[0])

    load(rentalProject, rentalMedian)


# Load data into MySQL accordingly
def load(rentalProject, rentalMedian):

    print("Rental Transactions: Loading data")

    # Transform data to list of values
    rentalProject = list(map(lambda x: tuple(x.values()), rentalProject))
    rentalMedian = list(map(lambda x: tuple(x.values()), rentalMedian))

    # Insert data
    db = DataWarehouse()
    db.insert_to_schema("main__RentalProject", rentalProject)
    db.insert_to_schema("main__RentalMedian", rentalMedian)


extract()


