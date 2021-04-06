
from todoist.api import TodoistAPI
from .todo_interface import Todo_interface 

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
        for item in self.client.state['items']:
            yield { 
                'id' : item.data['id'],
                'content' : item.data['content'],
                'due': item.data['due'],
                'project_name': self.__getProjectName(item.data['project_id'])
                }

    def getProjects(self):
        return self.client.state['projects']

    def addItem(self, value, due):
        self.client.items.add( value, due = due)
        self.commitChanges()

    def completeTask(self, task_id):
        task = self.__getTaskById(task_id)
        task.complete()
        self.commitChanges()
    
    def __getTaskById(self, id):
        for item in self.client_handler.getItems():
            if item.data['id'] == int(id):
                return item

    def __getProjectName(self, project_id):
        project = [ project for project in self.getProjects() if project.data['id'] == project_id ]
        if len(project) > 0:
            return project[0].data['name']
