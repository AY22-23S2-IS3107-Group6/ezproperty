from ..lake import DataLake
from ..warehouse import DataWarehouse
from .boilerplate import BoilerplatePipeline
from .carparkPublic import CarparkPublicPipeline
from .carparkSeason import CarparkSeasonPipeline
from .districtInfo import DistrictInfoPipeline
from .hawkerCentre import HawkerCentrePipeline
from .primarySchool import PrimarySchoolPipeline
from .propertyInfo import PropertyInformationPipeline
from .propertyTransaction import PropertyTransactionPipeline
from .rentalPropertyMedian import RentalPropertyMedianPipeline
from .supermarket import SupermarketPipeline
from .trainStation import TrainStationPipeline

if __name__ == "__main__":
    print(f"Pipeline | {'Start'.ljust(25)} | Re-create Datawarehouse")
    DataWarehouse(True, True)
    DataLake(True)
    # BoilerplatePipeline()
    # CarparkPublicPipeline()
    # CarparkSeasonPipeline()
    # DistrictInfoPipeline()
    # HawkerCentrePipeline()
    # PrimarySchoolPipeline()
    # PropertyInformationPipeline()
    # PropertyTransactionPipeline()
    # RentalPropertyMedianPipeline()
    SupermarketPipeline()
    TrainStationPipeline()