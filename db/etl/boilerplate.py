import pymongo
from .pipeline import Pipeline

class BoilerplatePipeline(Pipeline):
    description = "Boilerplate"
    schedule_interval = "@weekly"
    tags = ['test']
    schema_name = "test__Test"

    def extract(self) -> list:
        data = [{"_id": "2", "col1": "row1", "col2": "row2"}]

        self.dl_loader(data, self.schema_name)
        
        # Proof that query works
        for x in self.dl.query(self.schema_name, [
            {"$match": {"col1": "row1"}},
            {"$project": {"_id": 0, "col2": 1}}
        ]):
            print(x)

        return self.dl_getter(self.schema_name)

    def transform(self, result: list) -> list:
        return result

    def load(self, result: list) -> None:
        self.dw_loader(result, self.schema_name)