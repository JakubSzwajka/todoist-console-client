from console_client import ConsoleClient
import typer 

app = typer.Typer()

client = ConsoleClient('todoist')

@app.command()
def list( ):
    client.printTasks()

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