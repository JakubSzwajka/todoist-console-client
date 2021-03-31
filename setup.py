from cx_Freeze import setup, Executable

base = None    

executables = [Executable("todoist/main.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "todoist",
    options = options,
    version = "0.1",
    description = 'test_build',
    executables = executables
)