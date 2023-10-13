from dependency_injector import containers, providers

from application.comparison.service.comparison_service import ComparisonService
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from persistance.services.path_service import PathService


class Services(containers.DeclarativeContainer):
    # Singletons
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    # Application services
    comparison_service = providers.Factory(AbstractComparisonService.register(ComparisonService),
                                           path_service=paths_service)
