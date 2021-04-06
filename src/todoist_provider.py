
from todoist.api import TodoistAPI
from todo_interface import Todo_interface 

class TodoistProvider(Todo_interface):
    ''' 
        Use this class only to provide todoist client for sync API. 
        It should hold every data, authorized by provided token. 
    '''
    
    def __init__(self, configuration):
        self.CONFIG = configuration
        self.client = self.getClient()

    def getClient(self):
        client = TodoistAPI(self.CONFIG['auth']['token'])
        client.sync()
        return client
        
    def sync(self):
        self.client.sync()

    def commitChanges(self):
        self.client.commit()

    def getItems(self):
        return self.client.state['items']
        
    def getProjects(self):
        return self.client.state['projects']

    def addItem(self, value, due):
        self.client.items.add( value, due = due)
        self.commitChanges()
    

    def getTaskById(self, id):
        for item in self.client_handler.getItems():
            if item.data['id'] == int(id):
                return item

    def completeTask(self, task_id):
        task = self.getTaskById(task_id)
        task.complete()
        self.commitChanges()

