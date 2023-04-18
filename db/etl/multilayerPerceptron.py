import requests
from .pipeline import Pipeline

class MultilayerPerceptronPipeline(Pipeline):
    schema_name = "ml__MultiLayerPerceptron"

    def extract(self) -> list:

        # need to load one sample data to create the db if its empty. then, stop loading
        # data = [{}]
         
        # self.dl_loader(data, self.schema_name)
        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        return result

# if __name__ == '__main__':
MultilayerPerceptronPipeline()
    