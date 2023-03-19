from .main import main_create, main_insert
from .ref import ref_create, ref_insert
from .amn import amn_create, amn_insert

create_queries = main_create + ref_create + amn_create
insert_queries = main_insert + ref_insert + amn_insert