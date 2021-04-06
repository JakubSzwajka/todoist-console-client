from datetime import datetime
import emoji
import json
import os
from tabulate import tabulate
import typer
from todoist_provider import TodoistProvider

class ConsoleClient:
    def __init__(self):
        self.configuration = self.getConfig() 
        self.client_handler = TodoistProvider( self.configuration )

        self.DONE_EMOJI = self.configuration['emoji']['done_emoji']
        self.NOT_DONE_EMOJI = self.configuration['emoji']['not_done_emoji']

    def getConfig(self, file_name = "config.json"):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        full_path = f"{cur_dir}/{file_name}"

        with open(full_path, 'r') as config_file:
            config_dict = json.loads(config_file.read())

        return config_dict['default']

    def getTodaysTasks(self):
        todays = [ ]
        
        for item in self.client_handler.getItems():
            if self.isOverdue(item) or self.isToday(item) or self.wasCompletedToday(item):
                todays.append(item.data)
        return todays

    def wasCompletedToday(self, item):
        if self.configuration['display']['show_todays_completed'] == True and item['date_completed']: 
            completed_date = datetime.strptime( item['date_completed'], '%Y-%m-%dT%H:%M:%SZ')
            if completed_date.date() == datetime.today().date(): 
                return True
        return False

    def isToday(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item.data['due'] != None and item.data['due']['date'] == todays_date

    def isOverdue(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item.data['due'] != None and item.data['due']['date'] <= todays_date and item.data['checked'] == 0

    def setToken(self, value):
        self.configuration['auth']['token'] = value
        config_file_path = self.getConfigPath('config.cfg')
        print(config_file_path)
        with open(config_file_path, 'w') as configfile:
            self.configuration.write(configfile)
        print(f'token set to {value}')

    def getConfigPath(self, file_name = 'config.cfg' ):
        current_path = os.path.dirname(os.path.realpath(__file__)) 
        current_path += "\\" + file_name
        return current_path 

    def sortTasks(self, tasks):
        return sorted(tasks, key = lambda i: (i['due']['date'], i['checked']), reverse=True)
        
    def getProjectName(self, project_id):
        project = [ project for project in self.client_handler.getProjects() if project.data['id'] == project_id ]
        if len(project) > 0:
            return project[0].data['name']

    def printTasks(self):
        tasks = self.sortTasks(self.getTodaysTasks())
        task_rows = []
        for task in tasks: 
            status = self.DONE_EMOJI if task['checked'] == 1 else self.NOT_DONE_EMOJI
            task_rows.append([emoji.emojize(status), task['id'], task['content'], task['due']['string'], self.getProjectName(task['project_id'])])
        
        headers = ['Done', 'ID', 'Task', 'Date','Project']
        typer.echo(tabulate(task_rows, headers=headers, showindex="always"))
        
    def addNewTask(self, value, date):
        due = {
            "date" : date
        }
        
        self.client_handler.addItem(value,due = due)
        
    def completeTask(self, task_id):
        self.client_handler.completeTask()
        
