from unittest import mock, TestCase
from src.providers.provider_factory import ProviderFactory
from src.providers.todo_interface import Todo_interface
from src.console_client import ConsoleClient

from datetime import datetime, timedelta

class MockedClient(Todo_interface):
    def __init__(self, configuration):
        super().__init__(configuration)

        self.mocked_items = [{ 
            'id' : i,
            'content' : f'sample_content_{i}',
            'checked' : 1,
            'due' : {
                'date' : datetime.today().strftime('%Y-%m-%d')
                }
            } for i in range(5)]

    def getClient(self):
        pass 

    def getItems(self):
        return self.mocked_items 

class TestCase(TestCase):
    @mock.patch.object(ProviderFactory, 'getClientHandler')
    def setUp(self, mock_client_factory):
        self.mocked_client = MockedClient( {'some_config': 'value'})
        mock_client_factory.return_value = self.mocked_client
        self.cut = ConsoleClient('todoist')
    
    def test_Should_Return_List_Of_Current_Tasks_Where_Every_is_For_Today(self):
        tasks = self.cut.getTodaysTasks()

        for task in tasks: 
            self.assertIn( task, self.mocked_client.mocked_items )
            
    def test_should_return_list_of_two_undone_tasks_for_today_out_of_4(self):
        # arrange 
        self.mocked_client.mocked_items[0]['due']['date'] = (datetime.today() + timedelta( days= 2 )).strftime('%Y-%m-%d')
        self.mocked_client.mocked_items[1]['due']['date'] = (datetime.today() + timedelta( days= 2 )).strftime('%Y-%m-%d')
        
        tasks = self.cut.getTodaysTasks()
        
        for task in self.mocked_client.mocked_items[2:]:
            self.assertIn( task, tasks )

    

'''
    1. Pobieranie danych w postaci listy

    2. Zamykanie zadania 
    
    3. Dodawanie zadania

'''