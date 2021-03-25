from todoist.api import TodoistAPI
from datetime import date, datetime
import configparser
import emoji
import os
from tabulate import tabulate

class TodoistConsoleClient:
    def __init__(self):
        self.CONFIG = self.getConfig()
        self.client = self.getClient()
        self.DONE_EMOJI = self.CONFIG['emoji']['DONE_EMOJI']
        self.NOT_DONE_EMOJI = self.CONFIG['emoji']['NOT_DONE_EMOJI']

    def getClient(self):
        client = TodoistAPI(self.CONFIG['auth']['token'])
        client.sync()
        return client

    def getTodaysTasks(self):
        todays = [ ]
        for item in self.client.state['items']:
            if self.isOverdue(item) or self.isToday(item) or self.wasCompletedToday(item):
                todays.append(item.data)
        return todays
    

    def wasCompletedToday(self, item):

        if self.CONFIG['display']['show_todays_completed'] in ['true', 'True'] and item['date_completed']: 
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
        self.CONFIG['auth']['token'] = value
        config_file_path = self.getConfigPath('config.cfg')
        print(config_file_path)
        with open(config_file_path, 'w') as configfile:
            self.CONFIG.write(configfile)
        print(f'token set to {value}')

    def getConfigPath(self, file_name = 'config.cfg' ):
        current_path = os.path.dirname(os.path.realpath(__file__)) 
        current_path += "\\" + file_name
        return current_path 

    def getConfig(self, path = 'config.cfg'):
        config = configparser.ConfigParser()
        config.read(self.getConfigPath(path))
        return config

    def sortTasks(self, tasks):
        return sorted(tasks, key = lambda i: (i['due']['date'], i['checked']), reverse=True)
        
    def printTasks(self):
        tasks = self.sortTasks(self.getTodaysTasks())
        task_rows = []
        for task in tasks: 
            status = self.DONE_EMOJI if task['checked'] == 1 else self.NOT_DONE_EMOJI
            task_rows.append([emoji.emojize(status), task['id'], task['content'], task['due']['string']])

        headers = ['Done', 'ID', 'Task', 'Date']
        print(tabulate(task_rows, headers=headers, showindex="always"))
        
    def addNewTask(self, value, date):
        due = {
            "date" : date
        }
        newitem = self.client.items.add(value,due = due)
        self.client.commit()

    def getTaskById(self, id):
        for item in self.client.state['items']:
            if item.data['id'] == int(id):
                return item
        
    def completeTask(self, task_id):
        item = self.getTaskById(task_id)
        item.complete()
        self.client.commit()
        print(f'Task {task_id} completed')
