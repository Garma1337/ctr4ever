# coding=utf-8

from ctr4ever.models.repository.modelrepository import ModelRepository
from ctr4ever.models.standardset import StandardSet


class StandardSetRepository(ModelRepository):

    def _get_model_class(self) -> type:
        return StandardSet
