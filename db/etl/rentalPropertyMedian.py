import requests
from ..utils import getUraApiHeaders
from .pipeline import Pipeline


class RentalPropertyMedianPipeline(Pipeline):
    description = "Loads Rental Property from URA API"
    schedule_interval = "@daily"
    tags = ['main']
    schema_name = "main__RentalPropertyMedian"

    def extract(self) -> list:
        data = requests.get(
            'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Rental_Median',
            headers=getUraApiHeaders()).json()['Result']

        self.dl_loader(data, self.schema_name)

        # Test query
        for x in self.dl.query_find(self.schema_name,
                                    {"project": "ELLIOT AT THE EAST COAST"}):
            print(x)

        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        validate_attributes = (
            lambda project:
            ('rentalMedian' in project) and ('street' in project) and
            ('x' in project) and ('project' in project) and
            ('y' in project) and project['rentalMedian'] != [])
        rentalProject = [
            project for project in result if validate_attributes(project)
        ]

        rentalMedian = []

        # Break into two tables
        for project in rentalProject:
            # Rename/Typecast
            project['x'] = float(project['x'])
            project['y'] = float(project['y'])
            project['_id'] = id(project['_id'])

            # Bring out all the rental medians (flatten) into a new json object
            for median in project['rentalMedian']:
                rentalMedian.append(median)
                # add foreign key linking to project
                median['rentalProject'] = project['_id']

            del project['rentalMedian']

        return [result, rentalMedian]

    def load(self, result: list) -> None:
        rentalProject = result[0]
        rentalMedian = result[1]
        self.dw_loader(rentalProject, "main__RentalProject")
        self.dw_loader(rentalMedian, "main__RentalMedian")


if __name__ == '__main__':
    RentalPropertyMedianPipeline()