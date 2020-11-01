from abc import ABCMeta, abstractmethod


class Controller(metaclass=ABCMeta):

    @abstractmethod
    def _initialize(self, arrInput=None):
        pass

    @abstractmethod
    def _execute(self):
        pass

    def runing(self, arrInput):
        self._initialize(arrInput)
        return self._execute()