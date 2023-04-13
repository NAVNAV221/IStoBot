import uuid
from typing import List

from Logics.logic import Logic
from consts.flows.flow import Types


class Flow(object):
    def __init__(self, name: str, logics: Types.FLOW_LOGICS):
        self._id = uuid.uuid4()
        self.name = name
        self.logics: Types.FLOW_LOGICS = logics

    def run(self):
        pass
