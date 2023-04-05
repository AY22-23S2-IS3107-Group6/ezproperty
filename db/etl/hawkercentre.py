import requests
from .pipeline import Pipeline


class HawkerCentrePipeline(Pipeline):
    schema_name = "amn__HawkerCentre"

    def extract(self) -> list:
        # Seems to be limited by MongoDB's 100 BSON limit
        # resp = requests.get(
        #     'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d'
        # )
        data = requests.get(
            'https://data.gov.sg/api/action/datastore_search?resource_id=8f6bba57-19fc-4f36-8dcf-c0bda382364d&limit=107'
        ).json()['result']['records']

        self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        for record in result:
            # Rename/Typecast
            record['name'] = record['name_of_centre']
            record['location'] = record['location_of_centre']
            record['type'] = record['type_of_centre']
            record['owner'] = record['owner']
            record['noOfStalls'] = int(record['no_of_stalls'])
            record['noOfCookedFoodStalls'] = int(
                record['no_of_cooked_food_stalls'])
            record['noOfMktProduceStalls'] = int(
                record['no_of_mkt_produce_stalls'])
            record['district'] = None

            # Project
            del record['name_of_centre']
            del record['location_of_centre']
            del record['type_of_centre']
            del record['_id']
            del record['owner']
            del record['no_of_stalls']
            del record['no_of_cooked_food_stalls']
            del record['no_of_mkt_produce_stalls']

        return result


if __name__ == '__main__':
    HawkerCentrePipeline()