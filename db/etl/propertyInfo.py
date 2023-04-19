import requests
from .pipeline import Pipeline


class PropertyInformationPipeline(Pipeline):
    description = "Loads Property Information from Data.gov"
    schedule_interval = "@monthly"
    tags = ['is3107g6','ref']
    schema_name = "ref__PropertyInformation"

    def extract(self) -> list:
        self.dl_delete_all(self.schema_name) # de-cache to prevent duplication
        data = requests.request(
            "GET",
            "https://data.gov.sg/dataset/9dd41b9c-b7d7-405b-88f8-61b9ca9ba224/resource/482bfa14-2977-4035-9c61-c85f871daf4e/data"
        ).json()['records']
        
        self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        # Map town to district
        tag_dict = {"Y": True, "N": False}
        town_dict = {
            "AMK": "ANG MO KIO",
            "BB": "BUKIT BATOK",
            "BD": "BEDOK",
            "BH": "BISHAN",
            "BM": "BUKIT MERAH",
            "BP": "BUKIT PANJANG",
            "BT": "BUKIT TIMAH",
            "CCK": "CHOA CHU KANG",
            "CL": "CLEMENTI",
            "CT": "CENTRAL AREA",
            "GL": "GEYLANG",
            "HG": "HOUGANG",
            "JE": "JURONG EAST",
            "JW": "JURONG WEST",
            "KWN": "KALLANG/WHAMPOA",
            "MP": "MARINE PARADE",
            "PG": "PUNGGOL",
            "PRC": "PASIR RIS",
            "QT": "QUEENSTOWN",
            "SB": "SEMBAWANG",
            "SGN": "SERANGOON",
            "SK": "SENGKANG",
            "TAP": "TAMPINES",
            "TG": "TENGAH",
            "TP": "TOA PAYOH",
            "WL": "WOODLANDS",
            "YS": "YISHUN"
        }

        for prop in result:

            prop["id"] = prop["_id"]
            prop["block"] = prop["blk_no"]
            #prop["street"] = prop["street"]

            # only year given, so int is sufficient
            prop["yearCompleted"] = int(prop["year_completed"])

            # integers
            prop["totalDwellingUnits"] = int(prop["total_dwelling_units"])
            prop["maxFloorLevel"] = int(prop["max_floor_lvl"])
            prop["oneRoomSold"] = int(prop["1room_sold"])
            prop["twoRoomSold"] = int(prop["2room_sold"])
            prop["threeRoomSold"] = int(prop["3room_sold"])
            prop["fourRoomSold"] = int(prop["4room_sold"])
            prop["fiveRoomSold"] = int(prop["5room_sold"])
            prop["execSold"] = int(prop["exec_sold"])
            prop["multigenSold"] = int(prop["multigen_sold"])
            prop["studioAptSold"] = int(prop["studio_apartment_sold"])
            prop["oneRoomRental"] = int(prop["1room_rental"])
            prop["twoRoomRental"] = int(prop["2room_rental"])
            prop["threeRoomRental"] = int(prop["3room_rental"])
            prop["otherRoomRental"] = int(prop["other_room_rental"])

            # changing tags to booleans
            prop["residentialTag"] = tag_dict[prop["residential"]]
            prop["commercialTag"] = tag_dict[prop["commercial"]]
            prop["mscpTag"] = tag_dict[prop["multistorey_carpark"]]
            prop["marketHawkerTag"] = tag_dict[prop["market_hawker"]]
            prop["precinctPavilionTag"] = tag_dict[prop["precinct_pavilion"]]
            prop["miscTag"] = tag_dict[prop["miscellaneous"]]

            # get town name from acronym
            prop["bldgContractTown"] = town_dict[prop["bldg_contract_town"]]

            # Project
            del prop['year_completed']
            del prop['multigen_sold']
            del prop['bldg_contract_town']
            del prop['multistorey_carpark']
            del prop['total_dwelling_units']
            del prop['blk_no']
            del prop['exec_sold']
            del prop['max_floor_lvl']
            del prop['residential']
            del prop['1room_sold']
            del prop['precinct_pavilion']
            del prop['other_room_rental']
            del prop['5room_sold']
            del prop['3room_sold']
            del prop['commercial']
            del prop['4room_sold']
            del prop['miscellaneous']
            del prop['studio_apartment_sold']
            del prop['2room_rental']
            del prop['2room_sold']
            del prop['1room_rental']
            del prop['3room_rental']
            del prop['market_hawker']
            del prop['_id']

        return result


if __name__ == '__main__':
    PropertyInformationPipeline()