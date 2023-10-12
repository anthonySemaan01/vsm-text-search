from dependency_injector import containers, providers

from persistance.services.path_service import PathService
from domain.contracts.repositories.abstract_path_service import AbstractPathService


class Services(containers.DeclarativeContainer):
    # Singletons
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

