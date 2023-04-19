import requests
from .pipeline import Pipeline

class MultilayerPerceptronPipeline(Pipeline):
    schema_name = "ml__MultiLayerPerceptron"

    def extract(self) -> list:

        # self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        return result

if __name__ == '__main__':
    MultilayerPerceptronPipeline()
    