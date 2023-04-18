import requests
from .pipeline import Pipeline


class SupermarketPipeline(Pipeline):
    description = "Loads Supermarkets from Data.gov"
    schedule_interval = "@monthly"
    tags = ['amenities']
    schema_name = "amn__Supermarket"

    def extract(self) -> list:
        # Seems to be limited by MongoDB's 100 BSON limit
        # resp = requests.get(
        #     'https://data.gov.sg/api/action/datastore_search?resource_id=3561a136-4ee4-4029-a5cd-ddf591cce643'
        # )

        # But this works and I can insert 228 supermarkets
        data = requests.get(
            'https://data.gov.sg/api/action/datastore_search?resource_id=3561a136-4ee4-4029-a5cd-ddf591cce643&limit=258'
        ).json()['result']['records']

        self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        for supermarket in result:
            # Rename/Typecast
            supermarket['licenceNo'] = supermarket['licence_num']
            supermarket['licenseeName'] = supermarket['licensee_name']
            supermarket['buildingName'] = supermarket['building_name']
            supermarket['blockHouseNo'] = supermarket['block_house_num']
            supermarket['level'] = supermarket['level_num']
            supermarket['unitNo'] = supermarket['unit_num']
            supermarket['streetName'] = supermarket['street_name']
            supermarket['postalCode'] = int(supermarket['postal_code'])
            supermarket['district'] = None

            # Project
            del supermarket['_id']
            del supermarket['licence_num']
            del supermarket['licensee_name']
            del supermarket['building_name']
            del supermarket['block_house_num']
            del supermarket['level_num']
            del supermarket['unit_num']
            del supermarket['street_name']
            del supermarket['postal_code']

        return result


if __name__ == '__main__':
    SupermarketPipeline()
