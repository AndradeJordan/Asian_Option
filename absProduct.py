import abc

class AbsProduct(abc.ABC):

    @abc.abstractmethod
    def simulation_Path(self):
        pass
    @abc.abstractmethod
    def premium_by_riemann_approximation(self):
        pass

    @abc.abstractmethod
    def premium_by_trapeze_approximation(self):
        pass

