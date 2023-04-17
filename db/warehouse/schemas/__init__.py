from .main import main_create, main_insert
from .ref import ref_create, ref_insert
from .amn import amn_create, amn_insert
from .test import test_create, test_insert

# create_queries = main_create + amn_create
# insert_queries = main_insert + amn_insert

create_queries = {**ref_create, **main_create, **amn_create, **test_create} 
insert_queries = {**ref_insert, **main_insert, **amn_insert, **test_insert} 
