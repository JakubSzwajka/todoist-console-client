from datetime import datetime
import emoji
import json
import os
from tabulate import tabulate
import typer
from .providers.todoist_provider import TodoistProvider
from .providers.provider_factory import ProviderFactory

class EmojisHandler(object):
    '''
        handler for emojis codes
    '''
    pass

class ConsoleClient:
    '''
        Generetes and handler for todo api and handle it in console
    '''
    def __init__(self, client_type):
        self.client_type = client_type
        
        self.configuration = self.__getConfig() 
        self.emojis = self.__getEmojis()
        self.client_handler = ProviderFactory.getClientHandler( self.client_type, self.configuration['auth']['provider'] )

        self.DONE_EMOJI = self.configuration['emoji']['done_emoji']
        self.NOT_DONE_EMOJI = self.configuration['emoji']['not_done_emoji']

    def getTodaysTasks(self):
        todays = [ ]
        for item in self.client_handler.getItems():
            if self.__isOverdue(item) or self.__isToday(item) or self.__wasCompletedToday(item):
                todays.append(item)
        return todays


    def setToken(self, value):
        self.configuration['auth']['token'] = value
        config_file_path = self.__getConfigPath('config.cfg')

        with open(config_file_path, 'w') as configfile:
            self.configuration.write(configfile)
        print(f'token set to {value}')


    def printTasks(self):
        tasks = self.__sortTasks(self.getTodaysTasks())
        task_rows = []
        for task in tasks: 
            status = self.DONE_EMOJI if task['checked'] == 1 else self.NOT_DONE_EMOJI
            task_rows.append([emoji.emojize(status), task['id'], task['content'], task['due']['string'], self.__getProjectName(task['project_id'])])
        
        headers = ['Done', 'ID', 'Task', 'Date','Project']
        typer.echo(tabulate(task_rows, headers=headers, showindex="always"))
        
    def addNewTask(self, value, date):
        due = {
            "date" : date
        }
        
        self.client_handler.addItem(value,due = due)
        
    def completeTask(self, task_id):
        self.client_handler.completeTask()

    def __getEmojis(self):
        emojis_instance = EmojisHandler()

        for emoji_key, emoji_value in self.configuration['emoji'].items():
            setattr(emojis_instance, emoji_key, emoji_value )

    def __getConfig(self, file_name = "config.json"):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        full_path = f"{cur_dir}/{file_name}"

        with open(full_path, 'r') as config_file:
            config_dict = json.loads(config_file.read())

        return config_dict[self.client_type]

    def __wasCompletedToday(self, item):
        if self.configuration['display']['show_todays_completed'] == True and item['date_completed']: 
            completed_date = datetime.strptime( item['date_completed'], '%Y-%m-%dT%H:%M:%SZ')
            if completed_date.date() == datetime.today().date(): 
                return True
        return False

    def __isToday(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item['due'] != None and item['due']['date'] == todays_date

    def __isOverdue(self, item):
        todays_date = datetime.today().strftime('%Y-%m-%d')
        return item['due'] != None and item['due']['date'] <= todays_date and item['checked'] == 0
   
    def __getConfigPath(self, file_name = 'config.cfg' ):
        current_path = os.path.dirname(os.path.realpath(__file__)) 
        current_path += "\\" + file_name
        return current_path 

    def __sortTasks(self, tasks):
        return sorted(tasks, key = lambda i: (i['due']['date'], i['checked']), reverse=True)

