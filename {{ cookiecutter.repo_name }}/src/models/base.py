# -*- coding: utf-8 -*-
from src.utils.params import Registrable


class BaseModel(Registrable):
    def __init__(self, l2_norm, learning_rate, optim):
        self.l2_norm = float(l2_norm)
        self.learning_rate = learning_rate
        self.optim = optim

    def inputs(self):
        raise NotImplementedError

    def build_graph(self):
        raise NotImplementedError

    def optimizer(self):
        raise NotImplementedError
