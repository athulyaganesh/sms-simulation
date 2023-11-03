import unittest
from unittest.mock import patch
import main

class TestMain(unittest.TestCase):

    @patch('builtins.input', return_value='1000')
    def test_get_num_messages_valid_input(self, mock_input):
        result = main.get_num_messages()
        self.assertEqual(result, 1000)

    @patch('builtins.input', return_value='default')
    def test_get_num_messages_default_input(self, mock_input):
        result = main.get_num_messages()
        self.assertEqual(result, 'default')

    @patch('builtins.input', return_value='1000')
    def test_get_update_interval_valid_input(self, mock_input):
        result = main.get_update_interval()
        self.assertEqual(result, 1000)

    @patch('builtins.input', return_value='default')
    def test_get_update_interval_default_input(self, mock_input):
        result = main.get_update_interval()
        self.assertEqual(result, 'default')

    @patch('builtins.input', return_value='5')
    def test_get_num_senders_valid_input(self, mock_input):
        result = main.get_num_senders()
        self.assertEqual(result, 5)

    @patch('builtins.input', side_effect=['0', '1', '2', '3', '4', '5'])
    def test_get_num_senders_invalid_then_valid_input(self, mock_input):
        result = main.get_num_senders()
        self.assertEqual(result, 1)

    @patch('builtins.input', return_value='default')
    def test_get_sender_configs_default_input(self, mock_input):
        result = main.get_sender_configs(3)
        self.assertEqual(result, [{'mean_processing_time': 'default', 'error_rate': 'default'},
                                  {'mean_processing_time': 'default', 'error_rate': 'default'},
                                  {'mean_processing_time': 'default', 'error_rate': 'default'}])

    @patch('builtins.input', side_effect=['-100', '0', '5'])
    def test_get_num_senders_negative_then_valid_input(self, mock_input):
        result = main.get_num_senders()
        self.assertEqual(result, 5)


    @patch('builtins.input', side_effect=['-1000', '0', '1000'])
    def test_get_update_interval_negative_then_valid_input(self, mock_input):
        result = main.get_update_interval()
        self.assertEqual(result, 1000)

    @patch('builtins.input', side_effect=['-1000', 'string', '0', '1000'])
    def test_get_num_messages_invalid_then_valid_input(self, mock_input):
        result = main.get_num_messages()
        self.assertEqual(result, 1000)

if __name__ == '__main__':
    unittest.main()
