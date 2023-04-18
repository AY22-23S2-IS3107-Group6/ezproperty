import requests
from ..utils import getUraApiHeaders
from .pipeline import Pipeline


class CarparkSeasonPipeline(Pipeline):
    description = "Loads Seasonal Carparks from URA API"
    schedule_interval = "@weekly"
    tags = ['is3107g6','amn']
    schema_name = "amn__CarparkSeason"

    def extract(self) -> list:
        data = requests.get(
            'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=Season_Car_Park_Details',
            headers=getUraApiHeaders()).json()['Result']

        self.dl_loader(data, self.schema_name)
        
        # Test query
        for x in self.dl.query_find(self.schema_name, {"ppCode": "GA002"}):
            print(x)

        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        validate_attributes = (lambda carpark: ('ppCode' in carpark) and
                               ('ppName' in carpark) and
                               ('vehCat' in carpark) and
                               ('monthlyRate' in carpark) and
                               ('parkingHrs' in carpark) and
                               ('ticketType' in carpark))
        result = [
            carpark for carpark in result if validate_attributes(carpark)
        ]

        validate_geometries = (lambda carpark: carpark['geometries'] != [])
        result = [
            carpark for carpark in result if validate_geometries(carpark)
        ]

        for carpark in result:
            # Rename/Typecast
            carpark['x'] = float(
                carpark['geometries'][0]['coordinates'].split(",")[0])
            carpark['y'] = float(
                carpark['geometries'][0]['coordinates'].split(",")[1])
            carpark['_id'] = id(carpark['_id'])
            carpark['monthlyRate'] = int(carpark['monthlyRate'])
            carpark['district'] = None

            # Project
            del carpark['geometries']
            # del carpark['_id'] # uncomment this code if we decide we don't need _id if we using our own pkeys

        return result


if __name__ == '__main__':
    CarparkSeasonPipeline()