from console_client import ConsoleClient
import typer 
import emoji
from tabulate import tabulate


app = typer.Typer()

client = ConsoleClient('todoist')
emojis = client.emojis

def printTasks(tasks):
        task_rows = []
        for task in tasks: 
            status = emoji.done_emoji if task['checked'] == 1 else emoji.not_done_emoji
            task_rows.append([emoji.emojize(status), task['id'], task['content'], task['due']['string'], task['project_name']])
        
        headers = ['Done', 'ID', 'Task', 'Date','Project']
        typer.echo(tabulate(task_rows, headers=headers, showindex="always"))

@app.command()
def list():
    tasks = client.getTodaysTasks()
    printTasks(tasks)

@app.command()
def add_task( task_text: str, date: str ):
    client.addNewTask( task_text, date)
    client.printTasks()

@app.command()
def complete( task_id: str ):
    client.completeTask(task_id)
    client.printTasks()

@app.command()
def set_token( token: str):
    client.set_token( token)

if __name__ == "__main__":
    app()