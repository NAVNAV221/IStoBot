import logging
import uuid

from consts.flows.flow import Types
from utils.project_logger import get_logger


class Flow(object):
    def __init__(self, name: str, logics: Types.FLOW_LOGICS=None):
        self.logger = get_logger()
        self._id = uuid.uuid4()
        self.name = name
        self.logics: Types.FLOW_LOGICS = logics

    def run(self):
        raise NotImplementedError("run function not implemented")
