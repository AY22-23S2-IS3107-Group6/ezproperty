from typing import List
from ..lake import DataLake
from ..warehouse import DataWarehouse
from .pipeline import Pipeline
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
from .multilayerPerceptron import MultilayerPerceptronPipeline


def get_all_pipelines(run_pipelines: bool = False) -> List[Pipeline]:
    return [
        # BoilerplatePipeline(run_pipelines),
        CarparkPublicPipeline(run_pipelines),
        CarparkSeasonPipeline(run_pipelines),
        DistrictInfoPipeline(run_pipelines),
        HawkerCentrePipeline(run_pipelines),
        PrimarySchoolPipeline(run_pipelines),
        PropertyInformationPipeline(run_pipelines),
        PropertyTransactionPipeline(run_pipelines),
        RentalPropertyMedianPipeline(run_pipelines),
        SupermarketPipeline(run_pipelines),
        TrainStationPipeline(run_pipelines),
        MultilayerPerceptronPipeline(run_pipelines)
    ]


if __name__ == "__main__":
    create_tables, drop_tables, run_pipelines = True, True, True
    print(f"Pipeline | {'Start'.ljust(25)}")
    DataWarehouse(create_tables, drop_tables)
    DataLake(drop_tables)
    get_all_pipelines(run_pipelines)