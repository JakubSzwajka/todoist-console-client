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

    def getClient(self): raise NotImplementedError

    def sync(self): raise NotImplementedError

    def commitChanges(self): raise NotImplementedError

    def getItems(self): raise NotImplementedError

    def getProjects(self): raise NotImplementedError
        
    def addItem(self): raise NotImplementedError

    def completeTask(self): raise NotImplementedError