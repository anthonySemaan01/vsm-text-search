from pydantic import BaseModel


class ApiPaths(BaseModel):
    data_input_txt_docs: str
    txt_indexing_table: str

