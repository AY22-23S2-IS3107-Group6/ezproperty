import pymongo
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from enum import Enum

from ..lake import DataLake
from ..warehouse import DataWarehouse

def extract():
    # selenium web driver
    # def parse(url):
    #     response = webdriver.Chrome()
    #     response.get(url)
    #     sleep(3)
    #     sourceCode=response.page_source
    #     return  sourceCode

    # # pass the string to a BeatifulSoup object
    # soup = BeautifulSoup(parse("https://propertyreviewsg.com/complete-primary-school-list/"), 'html.parser')

    # # web scraping
    # table = soup.find('table', class_='tablepress tablepress-id-66 dataTable no-footer')

    # df = pd.DataFrame(columns=['schoolName', 'schoolChineseName', 'sap', 'gep', 'gender', 'affiliatedSecondary', 'area', 'address'])

    # for row in table.tbody.find_all('tr'):
    #     # find all data for each column
    #     columns = row.find_all('td')

    #     if (columns != []):
    #         schoolName = columns[0].text.strip()
    #         schoolChineseName = columns[1].text.strip()
    #         sap = columns[2].text.strip()
    #         gep = columns[3].text.strip()
    #         gender = columns[4].text.strip()
    #         affiliatedSecondary = columns[5].text.strip()
    #         area = columns[6].text.strip()
    #         address = columns[7].text.strip()

    #         df = pd.concat([df, pd.DataFrame.from_records([{
    #             'schoolName': schoolName,
    #             'schoolChineseName': schoolChineseName,
    #             'sap': sap,
    #             'gep': gep,
    #             'gender': gender,
    #             'affiliatedSecondary': affiliatedSecondary,
    #             'area': area,
    #             'address': address,
    #         }])])
    
    # # check data
    # print("Check web scraped data")
    # print(df.head())

    db = DataLake()
    # db.insert_to_schema("amn__PrimarySchool", df.to_dict('records'))

    testResult = db.query_find("amn__PrimarySchool", 
        { "schoolName": "Ai Tong School" }
    )

    # Proof that query works
    for x in testResult:
        print(x)

    result = db.query_find("amn__PrimarySchool", 
        {}
    )
    
    transform(result)


def transform(result):

    result = list(result)

    # Transform data accordingly
    print("Test: Transforming data")
    for school in result:
        if not school['sap']:
            school['sap'] = False
        else:
            school['sap'] = True

        if not school['gep']:
            school['gep'] = False
        else:
            school['gep'] = True

        school['_id'] = id(school['_id']) # using python generated _id for now since cant find a suitable pkey

    load(result)


def load(result):

    # Load data into MySQL accordingly
    print("Test: Loading data")
    # print(result)

    result = list(map(lambda x: tuple(x.values()), result))

    # Insert data
    db = DataWarehouse(True,True)
    db.insert_to_schema("amn__PrimarySchool", result)

    # Query data using SQL
    result = db.query('''
        SELECT * FROM amn__PrimarySchool
    ''')
    print(result[0])


extract()