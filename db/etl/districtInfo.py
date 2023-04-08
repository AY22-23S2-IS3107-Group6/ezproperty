import json
from .pipeline import Pipeline


class DistrictInfoPipeline(Pipeline):
    description = "Loads District Info natively"
    schedule_interval = None
    tags = ['ref']
    schema_names = ["ref__District", "ref__Town", "ref__PostalCode"]

    def extract(self) -> list:
        
        # Data
        districts = [
            {"district": 1}, {"district": 2}, {"district": 3}, {"district": 4}, {"district": 5}, {"district": 6}, {"district": 7},
            {"district": 8}, {"district": 9}, {"district": 10}, {"district": 11}, {"district": 12}, {"district": 13}, {"district": 14},
            {"district": 15}, {"district": 16}, {"district": 17}, {"district": 18}, {"district": 19}, {"district": 20}, {"district": 21},
            {"district": 22}, {"district": 23}, {"district": 24}, {"district": 25}, {"district": 26}, {"district": 27}, {"district": 28}
        ]

        towns = [
            {"town": "Raffles Place", "district": 1}, {"town": "Cecil", "district": 1}, {"town": "Marina", "district": 1}, {"town": "People's Park", "district": 1}, 
            {"town": "Anson", "district": 2}, {"town": "Tanjong Pagar", "district": 2},
            {"town": "Queenstown", "district": 3}, {"town": "Tiong Bahru", "district": 3}, 
            {"town": "Telok Blangah", "district": 4}, {"town": "Harbourfront", "district": 4}, 
            {"town": "Pasir Panjang", "district": 5}, {"town": "Hong Leong Garden", "district": 5}, {"town": "Clementi New Town", "district": 5}, 
            {"town": "High Street", "district": 6}, {"town": "Beach Road (part)", "district": 6},
            {"town": "Middle Road", "district": 7}, {"town": "Golden Mile", "district": 7}, 
            {"town": "Little India", "district": 8},
            {"town": "Orchard", "district": 9}, {"town": "Cairnhill", "district": 9}, {"town": "River Valley", "district": 9},
            {"town": "Ardmore", "district": 10}, {"town": "Bukit Timah", "district": 10}, {"town": "Holland Road", "district": 10}, {"town": "Tanglin", "district": 10},
            {"town": "Watten Estate", "district": 11}, {"town": "Novena", "district": 11}, {"town": "Thomson", "district": 11},
            {"town": "Balestier", "district": 12}, {"town": "Toa Payoh", "district": 12}, {"town": "Serangoon", "district": 3},
            {"town": "Macpherson", "district": 13}, {"town": "Braddell", "district": 13},
            {"town": "Geylang", "district": 14}, {"town": "Eunos", "district": 14},
            {"town": "Katong", "district": 15}, {"town": "Joo Chiat", "district": 15}, {"town": "Amber Road", "district": 15},
            {"town": "Bedok", "district": 16}, {"town": "Upper East Coast", "district": 16}, {"town": "Eastwood", "district": 16}, {"town": "Kew Drive", "district": 16},
            {"town": "Loyang", "district": 17}, {"town": "Changi", "district": 17},
            {"town": "Tampines", "district": 18}, {"town": "Pasir Ris", "district": 18},
            {"town": "Serangoon Garden", "district": 19}, {"town": "Hougang", "district": 19}, {"town": "Punggol", "district": 19},
            {"town": "Bishan", "district": 20}, {"town": "Ang Mo Kio", "district": 20},
            {"town": "Upper Bukit Timah", "district": 21}, {"town": "Clementi Park", "district": 21}, {"town": "Ulu Pandan", "district": 21},
            {"town": "Jurong", "district": 22}, 
            {"town": "Hillview", "district": 23}, {"town": "Dairy Farm", "district": 23}, {"town": "Bukit Panjang", "district": 23}, {"town": "Choa Chu Kang", "district": 23}, 
            {"town": "Lim Chu Kang", "district": 24}, {"town": "Tengah", "district": 24}, 
            {"town": "Kranji", "district": 25}, {"town": "Woodgrove", "district": 25}, 
            {"town": "Upper Thomson", "district": 26}, {"town": "Springleaf", "district": 26}, 
            {"town": "Yishun", "district": 27}, {"town": "Sembawang", "district": 27}, 
            {"town": "Seletar", "district": 28}
        ]

        postalCodes = [
            {"district": 1, "postalCodeStart": 1, "postalCodeEnd": 6},
            {"district": 2, "postalCodeStart": 7, "postalCodeEnd": 8},
            {"district": 3, "postalCodeStart": 14, "postalCodeEnd": 16},
            {"district": 4, "postalCodeStart": 9, "postalCodeEnd": 10},
            {"district": 5, "postalCodeStart": 11, "postalCodeEnd": 13},
            {"district": 6, "postalCodeStart": 17, "postalCodeEnd": 17},
            {"district": 7, "postalCodeStart": 18, "postalCodeEnd": 19},
            {"district": 8, "postalCodeStart": 20, "postalCodeEnd": 21},
            {"district": 9, "postalCodeStart": 22, "postalCodeEnd": 23},
            {"district": 10, "postalCodeStart": 24, "postalCodeEnd": 27},
            {"district": 11, "postalCodeStart": 28, "postalCodeEnd": 30},
            {"district": 12, "postalCodeStart": 31, "postalCodeEnd": 33},
            {"district": 13, "postalCodeStart": 34, "postalCodeEnd": 37},
            {"district": 14, "postalCodeStart": 38, "postalCodeEnd": 41},
            {"district": 15, "postalCodeStart": 42, "postalCodeEnd": 45},
            {"district": 16, "postalCodeStart": 46, "postalCodeEnd": 48},
            {"district": 17, "postalCodeStart": 49, "postalCodeEnd": 50},
            {"district": 17, "postalCodeStart": 81, "postalCodeEnd": 81},
            {"district": 18, "postalCodeStart": 51, "postalCodeEnd": 52},
            {"district": 19, "postalCodeStart": 53, "postalCodeEnd": 55},
            {"district": 19, "postalCodeStart": 82, "postalCodeEnd": 82},
            {"district": 20, "postalCodeStart": 56, "postalCodeEnd": 57},
            {"district": 21, "postalCodeStart": 58, "postalCodeEnd": 59},
            {"district": 22, "postalCodeStart": 60, "postalCodeEnd": 64},
            {"district": 23, "postalCodeStart": 65, "postalCodeEnd": 68},
            {"district": 24, "postalCodeStart": 69, "postalCodeEnd": 71},
            {"district": 25, "postalCodeStart": 72, "postalCodeEnd": 73},
            {"district": 26, "postalCodeStart": 77, "postalCodeEnd": 78},
            {"district": 27, "postalCodeStart": 75, "postalCodeEnd": 76},
            {"district": 28, "postalCodeStart": 79, "postalCodeEnd": 80}
        ]

        self.dl_loader(districts, self.schema_names[0])
        self.dl_loader(towns, self.schema_names[1])
        self.dl_loader(postalCodes, self.schema_names[2])
        return [self.dl_getter(schema) for schema in self.schema_names]

    def transform(self, result: list) -> list:
        # no x and y values yet

        for schema in result:
            for x in schema:
                # Project
                del x['_id']

        return result

    def load(self, result: list) -> None:
        for idx, schema in enumerate(self.schema_names):
            self.dw_loader(result[idx], schema)


if __name__ == '__main__':
    DistrictInfoPipeline()