from pydantic import BaseModel


class KMeansClusteringRequest(BaseModel):
    directory_name: str
