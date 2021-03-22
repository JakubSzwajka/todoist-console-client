from todoist.api import TodoistAPI
from datetime import datetime
import emoji
import click
import configparser
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
            if self.isOverdue(item) or self.isToday(item):
                todays.append(item.data)
        return todays
    
    def isToday(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item.data['due'] != None and item.data['due']['date'] == todays_date

    def isOverdue(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item.data['due'] != None and item.data['due']['date'] <= todays_date and item.data['checked'] == 0

    def setToken(self, value):
        self.CONFIG['auth']['token'] = value
        with open('config.cfg', 'w') as configfile:
            self.CONFIG.write(configfile)
        print(f'token set to {value}')

    def getConfig(self, path = 'config.cfg'):
        config = configparser.ConfigParser()
        config.read(path)
        return config

    def printTasks(self):
        tasks = sorted(self.getTodaysTasks(), key = lambda i: (i['due']['date']))
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

@click.command()
@click.option(
    "--set-token", default=None, required=False
)
@click.option(
    "--add", default=False, required=None
)
@click.option(
    "--date", default=lambda : datetime.today().strftime('%Y-%m-%d'), required= False
)
@click.option(
    "--complete", default=None, required=False
)
def main(set_token, add, date, complete):
    client = TodoistConsoleClient()

    if set_token != None:
        client.setToken(set_token)
        return 
    elif add:
        client.addNewTask(add, date)
    elif complete:
        client.completeTask(complete)
    else: 
        client.printTasks()

if __name__ == "__main__":
    main()        
    