from todoist_console_client import TodoistConsoleClient
from datetime import datetime
import click
import sys

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