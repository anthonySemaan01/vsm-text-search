from dependency_injector import containers, providers

from application.clustering.service.clustering_service import ClusteringService
from application.comparison.service.comparison_service import ComparisonService
from core.info_retrieval.info_retrieval_service import InfoRetrievalService
from core.vsm.vsm_service import VSMService
from core.vsm.vsm_similarity_service import VSMSimilarityService
from core.vsm.vsm_weight_service import VSMWeightService
from domain.contracts.repositories.abstract_path_service import AbstractPathService
from domain.contracts.services.abstract_clustering_service import AbstractClusteringService
from domain.contracts.services.abstract_comparison_service import AbstractComparisonService
from domain.contracts.services.abstract_info_retrieval_service import AbstractInfoRetrievalService
from domain.contracts.services.abstract_vsm_service import AbstractVSMService
from domain.contracts.services.abstract_vsm_similarity_service import AbstractVSMSimilarityService
from domain.contracts.services.abstract_vsm_weight_service import AbstractVSMWeightService
from persistance.services.path_service import PathService


class Services(containers.DeclarativeContainer):
    # Singletons
    paths_service = providers.Singleton(AbstractPathService.register(PathService))

    vsm_similarity_service = providers.Factory(AbstractVSMSimilarityService.register(VSMSimilarityService),
                                               path_service=paths_service)
    vsm_weight_service = providers.Factory(AbstractVSMWeightService.register(VSMWeightService),
                                           path_service=paths_service)

    vsm_service = providers.Factory(AbstractVSMService.register(VSMService),
                                    path_service=paths_service, vsm_weight_service=vsm_weight_service,
                                    vsm_similarity_service=vsm_similarity_service)

    info_retrieval_service = providers.Factory(AbstractInfoRetrievalService.register(InfoRetrievalService),
                                               path_service=paths_service, vsm_service=vsm_service)

    # Application services
    comparison_service = providers.Factory(AbstractComparisonService.register(ComparisonService),
                                           path_service=paths_service, vsm_service=vsm_service,
                                           info_retrieval_service=info_retrieval_service)

    clustering_service = providers.Factory(AbstractClusteringService.register(ClusteringService),
                                           paths_service=paths_service)
