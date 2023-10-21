from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile

from containers import Services
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService

router = APIRouter()


@router.get("/compute_txt_indexing_table")
@inject
def compute_txt_indexing_table(
        info_retrieval_service: AbstractInfoRetrievalService = Depends(
            Provide[Services.info_retrieval_service])):
    info_retrieval_service.compute_txt_indexing_table()


@router.post("/add_txt_file")
@inject
def add_txt_file(file: UploadFile,
                 info_retrieval_service: AbstractInfoRetrievalService = Depends(
                     Provide[Services.info_retrieval_service])):
    info_retrieval_service.add_file_to_txt_collection(file=file, with_indexing=True)
