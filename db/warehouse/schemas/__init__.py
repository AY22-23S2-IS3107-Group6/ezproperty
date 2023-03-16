from .main import main_create, main_insert
from .amn import amn_create, amn_insert

create_queries = main_create + amn_create
insert_queries = main_insert + amn_insert