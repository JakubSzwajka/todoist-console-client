import tkinter as tk
import requests
from todoist.api import TodoistAPI
from todoist.models import Item
from datetime import datetime

def getClient():
    token = 'baaa494629a69edc5e8274e9be151ef34f3ce6ae'
    client = TodoistAPI(token)
    return client

def getTodaysTasks():
    client = getClient()
    todays_date = datetime.today().strftime('%Y-%m-%d')
    todays = [ ]
    for item in client.state['items']:
        if item.data['due'] != None and item.data['due']['date']  == todays_date:
            todays.append( item.data )
    return todays 

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.entrythingy = tk.Entry()
        self.entrythingy.pack()

        # Create the application variable.
        self.contents = tk.StringVar()
        # Set it to some value.
        self.contents.set("this is a variable")
        # Tell the entry widget to watch this variable.
        self.entrythingy["textvariable"] = self.contents

        # Define a callback for when the user hits return.
        # It prints the current value of the variable.
        self.entrythingy.bind('<Key-Return>',
                             self.print_contents)

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

# root = tk.Tk()
# myapp = App(root)
# myapp.mainloop()

if __name__ == "__main__":
    tasks = getTodaysTasks()
