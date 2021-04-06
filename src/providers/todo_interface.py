from abc import abstractmethod, ABCMeta

class Todo_interface:
    '''
        Interface for different TODO list apps / APIs 

    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, configuration):  
        self.CONFIG = configuration
        self.client = self.getClient()

    @abstractmethod
    def getClient(self): raise NotImplementedError

    @abstractmethod
    def sync(self): raise NotImplementedError

    @abstractmethod
    def commitChanges(self): raise NotImplementedError

    @abstractmethod
    def getItems(self): raise NotImplementedError

    @abstractmethod
    def getProjects(self): raise NotImplementedError
        
    @abstractmethod
    def addItem(self): raise NotImplementedError

    @abstractmethod
    def completeTask(self): raise NotImplementedError