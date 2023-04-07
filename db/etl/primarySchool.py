import pandas as pd
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from .pipeline import Pipeline


class PrimarySchoolPipeline(Pipeline):
    description = "Loads Primary Schools from 3rd Party"
    schedule_interval = "@monthly"
    tags = ['amn']
    schema_name = "amn__PrimarySchool"

    def extract(self) -> list:

        # pass the string to a BeatifulSoup object
        soup = BeautifulSoup(
            self.parse(
                "https://propertyreviewsg.com/complete-primary-school-list/"),
            'html.parser')

        # web scraping
        table = soup.find(
            'table', class_='tablepress tablepress-id-66 dataTable no-footer')

        df = pd.DataFrame(columns=[
            'schoolName', 'schoolChineseName', 'sap', 'gep', 'gender',
            'affiliatedSecondary', 'area', 'address'
        ])

        for row in table.tbody.find_all('tr'):
            # find all data for each column
            columns = row.find_all('td')

            if (columns != []):
                schoolName = columns[0].text.strip()
                schoolChineseName = columns[1].text.strip()
                sap = columns[2].text.strip()
                gep = columns[3].text.strip()
                gender = columns[4].text.strip()
                affiliatedSecondary = columns[5].text.strip()
                area = columns[6].text.strip()
                address = columns[7].text.strip()

                df = pd.concat([
                    df,
                    pd.DataFrame.from_records([{
                        'schoolName': schoolName,
                        'schoolChineseName': schoolChineseName,
                        'sap': sap,
                        'gep': gep,
                        'gender': gender,
                        'affiliatedSecondary': affiliatedSecondary,
                        'area': area,
                        'address': address,
                    }])
                ])

        data = df.to_dict('records')

        # Test query
        for x in self.dl.query_find(self.schema_name,
                                    {"schoolName": "Ai Tong School"}):
            print(x)

        self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        for school in result:
            # Rename/Typecast
            school['sap'] = bool(school['sap'])
            school['gep'] = bool(school['gep'])
            school['_id'] = id(school['_id'])

        return result

    def parse(self, url: str):
        response = webdriver.Chrome()
        response.get(url)
        sleep(3)
        sourceCode = response.page_source
        return sourceCode


if __name__ == '__main__':
    PrimarySchoolPipeline()