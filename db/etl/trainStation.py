import pandas as pd
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from .pipeline import Pipeline


class TrainStationPipeline(Pipeline):
    schema_name = "amn__TrainStation"

    def extract(self) -> list:
        # make a request to the site and get it as a string
        markup = requests.get(
            f'https://github.com/hxchua/datadoubleconfirm/blob/master/datasets/mrtsg.csv'
        ).text

        # pass the string to a BeatifulSoup object
        soup = BeautifulSoup(markup, 'html.parser')

        # web scraping
        table = soup.find('table',
                          class_='js-csv-data csv-data js-file-line-container')

        df = pd.DataFrame(columns=[
            'id', 'stationName', 'stationNo', 'x', 'y', 'latitude',
            'longitude', 'colour'
        ])

        for row in table.tbody.find_all('tr'):
            # find all data for each column
            columns = row.find_all('td')

            if (columns == []): continue

            id = columns[1].text.strip()
            stationName = columns[2].text.strip()
            stationNo = columns[3].text.strip()
            x = columns[4].text.strip()
            y = columns[5].text.strip()
            latitude = columns[6].text.strip()
            longitude = columns[7].text.strip()
            colour = columns[8].text.strip()

            df = pd.concat([
                df,
                pd.DataFrame.from_records([{
                    'id': id,
                    'stationName': stationName,
                    'stationNo': stationNo,
                    'x': x,
                    'y': y,
                    'latitude': latitude,
                    'longitude': longitude,
                    'colour': colour,
                }])
            ])

        data = df.to_dict('records')

        self.dl_loader(data, self.schema_name)

        # Test query
        for x in self.dl.query_find(self.schema_name, {"stationNo": "EW5"}):
            print(x)

        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        for trainStation in result:
            trainStation['x'] = Decimal(trainStation['x'])
            trainStation['y'] = Decimal(trainStation['y'])
            trainStation['latitude'] = Decimal(trainStation['latitude'])
            trainStation['longitude'] = Decimal(trainStation['longitude'])
            trainStation['_id'] = id(trainStation['_id'])
            trainStation['district'] = None
            del trainStation['id']

        return result


if __name__ == '__main__':
    TrainStationPipeline()