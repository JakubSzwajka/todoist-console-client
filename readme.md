# Todoist Console Client ⌨

CLI app for todoist. Integrate your todoist account by token and access your task list in console. 

If you want to read more about it, check out my [blog]() and posts related. 

## commands

*  **to set the token** use ``` todoist set_token {your_token}```
*  **to get tasks** that are/were for today and those overdue use ``` todoist list```
*  **to add task**
default value for date is current day so you don't have to use --date flag. ```todoist add_task {name of your task} {yyy-mm-dd}```
* **to complete task** ```todoist complete {id_of_task}```

## Resources: 

* [typer repo](https://github.com/tiangolo/typer)
* [todoist sync API](https://developer.todoist.com/sync/v8/#overview)