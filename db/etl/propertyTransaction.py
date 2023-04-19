import datetime
import requests
from ..utils import chunks, getUraApiHeaders
from .pipeline import Pipeline


class PropertyTransactionPipeline(Pipeline):
    description = "Loads Property Transactions from URA API and Data.gov.sg"
    schedule_interval = "@daily"
    tags = ['is3107g6','main']
    schema_name = "main__PropertyTransaction"

    def extract(self) -> list:
        apiHeader = getUraApiHeaders()

        # Private Property Transcations
        dataPrivate = []
        dataPrivate.append(
            requests.get(
                'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=1',
                headers=apiHeader).json()['Result'])
        dataPrivate.append(
            requests.get(
                'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=2',
                headers=apiHeader).json()['Result'])
        dataPrivate.append(
            requests.get(
                'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=3',
                headers=apiHeader).json()['Result'])
        dataPrivate.append(
            requests.get(
                'https://www.ura.gov.sg/uraDataService/invokeUraDS?service=PMI_Resi_Transaction&batch=4',
                headers=apiHeader).json()['Result'])

        # HDB Resale Property Transactions
        dataPublic = []
        dataPublic.append(
            requests.get(
                'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=125000'
            ).json()["result"]["records"])
        dataPublic.append(
            requests.get(
                'https://data.gov.sg/api/action/datastore_search?resource_id=1b702208-44bf-4829-b620-4615ee19b57c&limit=25000'
            ).json()["result"]["records"])
        dataPublic.append(
            requests.get(
                'https://data.gov.sg/api/action/datastore_search?resource_id=83b2fc37-ce8c-4df4-968b-370fd818138b&limit=25000'
            ).json()["result"]["records"])
        dataPublic.append(
            requests.get(
                'https://data.gov.sg/api/action/datastore_search?resource_id=8c00bf08-9124-479e-aeca-7cc411d884c4&limit=25000'
            ).json()["result"]["records"])

        for dataset in dataPrivate:
            self.dl_loader(dataset, "main__PropertyTransactionsPrivate")
        for dataset in dataPublic:
            self.dl_loader(dataset, "main__PropertyTransactionsPublic")

        return [
            self.dl_getter("main__PropertyTransactionsPrivate"),
            self.dl_getter("main__PropertyTransactionsPublic")
        ]

    def transform(self, result: list) -> list:
        tempPrivate = result[0]
        tempResale = result[1]

        townDistrictMap = { t["town"].upper() : t["district"] for t in self.dl_getter("ref__Town")}

        filteredResale = []
        filteredPrivateProjects = []
        filteredPrivateTransactions = []

        for transaction in tempResale:
            if ('street_name' in transaction) and (
                    'storey_range'
                    in transaction) and ('flat_type' in transaction) and (
                        'floor_area_sqm' in transaction) and (
                            'resale_price' in transaction) and (
                                'month' in transaction) and ('remaining_lease'
                                                             in transaction):
                filteredResale.append(transaction)

        # Resale: Getting key/values we want
        for transaction in filteredResale:
            transaction['district'] = townDistrictMap.get(transaction['town'], 1)  # need map town to district
            transaction['street'] = transaction['street_name']
            transaction['floorRangeStart'] = int(
                transaction['storey_range'].split(" ")[0])
            transaction['floorRangeEnd'] = int(
                transaction['storey_range'].split(" ")[2])
            transaction['propertyType'] = transaction['flat_type'] + "HDB"
            transaction['area'] = float(transaction['floor_area_sqm'])
            transaction['price'] = float(transaction['resale_price'])

            # Convert date to SQL formatting
            year = int(transaction['month'].split("-")[0])
            month = int(transaction['month'].split("-")[1])
            date = datetime.datetime(year, month, 1)
            dateSql = date.strftime('%Y-%m-%d')

            transaction['transactionDate'] = dateSql
            transaction['tenure'] = int(transaction['remaining_lease'].split(
                " ")[0])  # only taking year for now
            transaction['resale'] = True

            # Code for no of room if want to add in
            # transaction['noOfRoom'] = int(3 if transaction['flat_type'].split(" ")[0] == "EXECUTIVE" else transaction['flat_type'].split(" ")[0])

            del transaction['block']
            del transaction['_id']
            del transaction['town']
            del transaction['street_name']
            del transaction['flat_type']
            del transaction['flat_model']
            del transaction['floor_area_sqm']
            del transaction['resale_price']
            del transaction['month']
            del transaction['remaining_lease']
            del transaction['lease_commence_date']
            del transaction['storey_range']

        for project in tempPrivate:
            checker = True
            for transaction in project['transaction']:
                if ('propertyType'
                        not in transaction) or ('area' not in transaction) or (
                            'price' not in transaction) or (
                                'tenure' not in transaction) or (
                                    'floorRange' not in transaction) or (
                                        'district' not in transaction) or (
                                            'contractDate' not in transaction):
                    checker = False

            if ('street' not in project):
                checker = False

            if checker:
                filteredPrivateProjects.append(project)

        for project in filteredPrivateProjects:
            for transaction in project['transaction']:

                # for reordering
                tempType = transaction['propertyType']
                del transaction['propertyType']
                tempArea = transaction['area']
                del transaction['area']
                tempPrice = transaction['price']
                del transaction['price']
                tempTenure = transaction['tenure']
                del transaction['tenure']

                # logic to manage B levels in floor range
                if (transaction['floorRange'].split("-")[0] == ""):
                    floorRangeStart = 0
                    floorRangeEnd = 0
                else:
                    if ("B" in transaction['floorRange'].split("-")[0]):
                        floorRangeStart = -int(
                            transaction['floorRange'].split("-")[0][1:])
                    else:
                        floorRangeStart = int(
                            transaction['floorRange'].split("-")[0])

                    if ("B" in transaction['floorRange'].split("-")[1]):
                        floorRangeEnd = -int(
                            transaction['floorRange'].split("-")[1][1:])
                    else:
                        floorRangeEnd = int(
                            transaction['floorRange'].split("-")[1])

                transaction['district'] = int(transaction['district'])
                transaction['street'] = project['street']
                transaction['floorRangeStart'] = floorRangeStart
                transaction['floorRangeEnd'] = floorRangeEnd
                transaction['propertyType'] = tempType
                transaction['area'] = float(tempArea)
                transaction['price'] = float(tempPrice)

                # Convert date to SQL formatting
                year = int("20" + transaction['contractDate'][-2:])
                month = int(transaction['contractDate'][:2])
                date = datetime.datetime(year, month, 1)
                dateSql = date.strftime('%Y-%m-%d')

                # Calculate tenure
                if isinstance(tempTenure, str):
                    tenure = 1000000
                elif tempTenure.split(" ")[-1] == "leasehold":
                    tenure = tempTenure.split(" ")[0]
                else:
                    leaseDur = int(tempTenure.split(" ")[0])
                    startYear = int(tempTenure.split(" ")[-1])
                    yearDiff = 2023 - startYear
                    tenure = leaseDur - yearDiff

                transaction['transactionDate'] = dateSql
                transaction['tenure'] = tenure
                transaction['resale'] = transaction['typeOfSale'] == 3

                if ('nettPrice' in transaction):
                    del transaction['nettPrice']
                del transaction['noOfUnits']
                del transaction['contractDate']
                del transaction['typeOfSale']
                del transaction['typeOfArea']
                del transaction['floorRange']

                filteredPrivateTransactions.append(transaction)

        # for transaction in combinedTransactions:
        #     if ('district' in transaction) and ('street' in transaction) and ('floorRangeStart' in transaction) and ('floorRangeEnd' in transaction) and ('propertyType' in transaction) and ('area' in transaction) and ('price' in transaction) and ('transactionDate' in transaction) and ('tenure' in transaction) and ('resale' in transaction):
        #         filteredCombinedTransactions.append(transaction)

        # print("Pre filter length", len(combinedTransactions))
        # print("Post filter length", len(filteredCombinedTransactions))

        return [filteredPrivateTransactions, filteredResale]

    def load(self, result: list) -> None:
        # private
        chunk_nos = 10
        chunk_generator = chunks(result[0], chunk_nos)
        for _ in range(chunk_nos):
           self.dw_loader(next(chunk_generator), self.schema_name)

        # public
        chunk_nos = 10
        chunk_generator = chunks(result[1], chunk_nos)
        for _ in range(chunk_nos):
           self.dw_loader(next(chunk_generator), self.schema_name)


if __name__ == '__main__':
    PropertyTransactionPipeline()