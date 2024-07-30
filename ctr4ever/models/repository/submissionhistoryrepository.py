# coding=utf-8

from ctr4ever.models.repository.submissionrepository import SubmissionRepository
from ctr4ever.models.submissionhistory import SubmissionHistory


class SubmissionHistoryRepository(SubmissionRepository):

    def _get_model_class(self) -> type:
        return SubmissionHistory
