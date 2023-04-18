import requests
from ..utils import getUraApiHeaders
from .pipeline import Pipeline


class CarparkPublicPipeline(Pipeline):
    description = "Loads Public Carparks from URA API"
    schedule_interval = "@weekly"
    tags = ['is3107g6','amn']
    schema_name = "amn__CarparkPublic"

    def extract(self) -> list:
        data = requests.get(
            'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Car_Park_Details',
            headers=getUraApiHeaders()).json()['Result']

        self.dl_loader(data, self.schema_name)
        
        # Test query
        for x in self.dl.query_find(self.schema_name, {"ppCode": "A0004"}):
            print(x)

        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        validate_attributes = (
            lambda carpark: ('weekdayMin' in carpark) and
            ('weekdayRate' in carpark) and ('ppCode' in carpark) and
            ('parkingSystem' in carpark) and ('ppName' in carpark) and
            ('vehCat' in carpark) and ('satdayMin' in carpark) and
            ('satdayRate' in carpark) and ('sunPHMin' in carpark) and
            ('sunPHRate' in carpark) and ('startTime' in carpark) and
            ('parkCapacity' in carpark) and ('endTime' in carpark))
        result = [
            carpark for carpark in result if validate_attributes(carpark)
        ]

        validate_geometries = (lambda carpark: carpark['geometries'] != [])
        result = [
            carpark for carpark in result if validate_geometries(carpark)
        ]

        # Flatten coordinates
        # Bring out into x and y key
        for carpark in result:
            # Rename/Typecast
            carpark['x'] = float(
                carpark['geometries'][0]['coordinates'].split(",")[0])
            carpark['y'] = float(
                carpark['geometries'][0]['coordinates'].split(",")[1])
            carpark['_id'] = id(carpark['_id'])
            carpark['weekdayRate'] = float(
                carpark['weekdayRate'][1:])  # removing $ sign
            carpark['weekdayMin'] = int(
                carpark['weekdayMin'][:-5])  # removing mins from back
            carpark['satdayRate'] = float(carpark['satdayRate'][1:])
            carpark['satdayMin'] = int(carpark['satdayMin'][:-5])
            carpark['sunPHRate'] = float(carpark['sunPHRate'][1:])
            carpark['sunPHMin'] = int(carpark['sunPHMin'][:-5])
            
            # Project
            del carpark['geometries']
            if 'remarks' in carpark:
                del carpark['remarks']
            # del carpark['_id'] # uncomment this code if we decide we don't need _id if we using our own pkeys

        # Merge objects with ppCode - hold off for now; prob better to minimise transformation and see what's needed during analyiss maybe
        # prob use double for loop and update function to merge

        return result


if __name__ == '__main__':
    CarparkPublicPipeline()
