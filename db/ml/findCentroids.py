import requests
from sqlalchemy import create_engine
import json
import pandas as pd
from ..lake import DataLake
from ..warehouse import DataWarehouse


# Define the JSON object
# Private Residential Properties Rental Contract
def findCentroids():

    # Load Private Residential Property Transactions
    property_transactions_json_str = '''
  {
    "Result": [{
      "project": "TURQUOISE",
      "marketSegment": "CCR",
      "transaction": [{
          "contractDate": "0715",
          "area": "203",
          "price": "2900000",
          "propertyType": "Condominium",
          "typeOfArea": "Strata",
          "tenure": "99 yrs lease commencing from 2007",
          "floorRange": "01-05",
          "typeOfSale": "3",
          "district": "04",
          "noOfUnits": "1"
        },
        {
          "contractDate": "0116",
          "area": "200",
          "price": "3014200",
          "propertyType": "Condominium",
          "typeOfArea": "Strata",
          "tenure": "99 yrs lease commencing from 2007",
          "floorRange": "01-05",
          "typeOfSale": "3",
          "district": "04",
          "noOfUnits": "1"
        }
      ],
      "street": "COVE DRIVE",
      "y": "24997.821719180001",
      "x": "28392.530515570001"
    }],
    "Status": "Success"
  }
  '''

    # Load Private Non-Landed Residential Properties Median Rentals by Name
    non_landed_properties_median_rentals_json_str = '''
      {
      "Result": [{
          "project": "MERAWOODS",
          "street": "HILLVIEW AVENUE",
          "rentalMedian": [{
              "median": 2.5,
              "psf25": 2.32,
              "psf75": 2.6,
              "district": "23",
              "refPeriod": "2014Q2"
            },
            {
              "median": 2.48,
              "psf25": 2.16,
              "psf75": 2.55,
              "district": "23",
              "refPeriod": "2014Q3"
            },
            {
              "median": 2.45,
              "psf25": 2.29,
              "psf75": 2.8,
              "district": "23",
              "refPeriod": "2012Q1"
            }
          ],
          "y": "37575.873911829997",
          "x": "19822.860634660001"
        },
        {
          "project": "ELLIOT AT THE EAST COAST",
          "street": "ELLIOT ROAD",
          "rentalMedian": [{
              "median": 3.32,
              "psf25": 2.8,
              "psf75": 3.46,
              "district": "15",
              "refPeriod": "2012Q3"
            },
            {
              "median": 2.92,
              "psf25": 2.63,
              "psf75": 3.45,
              "district": "15",
              "refPeriod": "2014Q2"
            },
            {
              "median": 3.19,
              "psf25": 2.79,
              "psf75": 3.46,
              "district": "15",
              "refPeriod": "2012Q2"
            }
          ],
          "y": "32635.6331629",
          "x": "38853.473729029998"
        }
      ],
      "Status": "Success"
    }
    
    '''

    # Load Residential Properties Rental Contract
    private_properties_rental_contract_json_str = '''
    {
      "Result": [{
          "project": "THOMSON RISE ESTATE",
          "street": "JALAN BERJAYA",
          "rental": [{
            "leaseDate": "0314",
            "propertyType": "Detached House",
            "areaSqm": "150-200",
            "areaSqft": "1500-2000",
            "rent": 4300,
            "district": "15"
          }],
          "y": "37250.512899840002",
          "x": "29360.426817729999"
        },
        {
          "project": "THE ESPIRA",
          "street": "LORONG L TELOK KURAU",
          "rental": [{
              "leaseDate": "0314",
              "propertyType": "Non-landed Properties",
              "areaSqm": "100-110",
              "areaSqft": "1100-1200",
              "rent": 3100,
              "district": "15",
              "noOfBedRoom": "3"
            },
            {
              "leaseDate": "0314",
              "propertyType": "Non-landed Properties",
              "areaSqm": "50-60",
              "areaSqft": "500-600",
              "rent": 2400,
              "district": "15",
              "noOfBedRoom": "1"
            }
          ],
          "y": "32747.030532890001",
          "x": "37045.353209170002"
        }
      ],
      "Status": "Success"
    }'''

    # Load Residential Property Units Sold by Developers
    properties_sold_by_developers_json_str = '''
    {
      "Result": [{
          "project": "LUXUS HILLS",
          "marketSegment": "OCR",
          "developer": "Singapore United Estates Pte Ltd",
          "street": "YIO CHU KANG ROAD/ANG MO KIO AVENUE 5/SELETAR ROAD",
          "developerSales": [{
            "highestPrice": 0,
            "soldToDate": 90,
            "unitsAvail": 236,
            "medianPrice": 0,
            "soldInMonth": 0,
            "launchedToDate": 90,
            "lowestPrice": 0,
            "refPeriod": "0913",
            "launchedInMonth": 0
          }],
          "district": "28",
          "y": "40264.704801180002",
          "x": "32524.18989369"
        },
        {
          "project": "BLOSSOM RESIDENCES",
          "marketSegment": "OCR",
          "developer": "Grand Isle Holdings Pte Ltd",
          "street": "SEGAR ROAD",
          "developerSales": [{
            "highestPrice": 0,
            "soldToDate": 601,
            "unitsAvail": 602,
            "medianPrice": 0,
            "soldInMonth": 0,
            "launchedToDate": 602,
            "lowestPrice": 0,
            "refPeriod": "0913",
            "launchedInMonth": 0
          }],
          "district": "23"
        }
      ],
      "Status": "Success"
    }

    '''

    # JSON implementation
    # Parse the JSON object into a Python dictionary
    data = json.loads(private_properties_rental_contract_json_str)

    # Create a dictionary to store the total x and y values and number of properties for each district
    district_data = {}

    # Iterate through the properties and calculate the total x and y values for each district
    for property in data["Result"]:
        # need to accomodate to rental or transaction or rentalMedian
        #  also cases when district is separate
        district = property["rental"][0]["district"]
        x = float(property["x"])
        y = float(property["y"])

        if district not in district_data:
            district_data[district] = {"x_total": x, "y_total": y, "count": 1}
        else:
            district_data[district]["x_total"] += x
            district_data[district]["y_total"] += y
            district_data[district]["count"] += 1

    # Iterate through the districts and calculate the average x and y values

    district_centroid = {}

    for district, data in district_data.items():
        # data is the array within each dictionary
        x_avg = data["x_total"] / data["count"]
        y_avg = data["y_total"] / data["count"]
        district_centroid[district] = {"x_avg": x_avg, "y_avg": y_avg}

        print("District:", district)
        print("Average x value and y value", district_centroid[district])
        # print("Average y value:", y_avg)


findCentroids()
