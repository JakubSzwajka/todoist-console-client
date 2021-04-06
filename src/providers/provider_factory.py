from .todoist_provider import TodoistProvider

class ProviderFactory:
    def getClientHandler(client_type, configuration):
        if client_type == 'todoist':
            return TodoistProvider( configuration )
        elif client_type == 'test': # for testing
            return None
        else:
            raise KeyError