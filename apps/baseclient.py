from abc import ABCMeta, abstractmethod

class BaseClient(object):

    __metadata__ = ABCMeta
    # def __init__(self, strDirConfig):
    #     self.strDirConfig = strDirConfig

    # @property
    @abstractmethod
    def controller(self):
        #this property will be supplied by the inheriting classes
        #individually
        pass

    @property    
    @abstractmethod
    def cli(self):
        pass

    @property    
    @abstractmethod
    def installer(self):
        pass

    @abstractmethod
    def gui(self):
        pass

    @abstractmethod
    def test(self):
        pass
