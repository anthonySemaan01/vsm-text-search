from pydantic import BaseModel


class ApiPaths(BaseModel):
    data_input_txt_docs: str
    txt_indexing_table: str
    uploaded_files: str
    xml_version_of_txt: str
    data_input_txt_docs_structured: str
    data_input_txt_docs_flat: str

