from queue import Queue
import unittest
from ProgressMonitor import ProgressMonitor
from Senders import Sender
import ProducerAndMessage 

class ProgressMonitorTest(unittest.TestCase):
    def test_initialization(self):
        senders_list = [Sender(), Sender()]
        progress_monitor = ProgressMonitor(senders_list)
        self.assertIsNotNone(progress_monitor)

    def test_update_interval(self):
        senders_list = [Sender(), Sender()]
        progress_monitor = ProgressMonitor(senders_list)
        self.assertEqual(progress_monitor.get_update_interval(), 5)

        progress_monitor.update_interval = 10
        self.assertEqual(progress_monitor.get_update_interval(), 10)

    def test_record(self):
        senders_list = [Sender(5, 50), Sender(4, 5)]
        message_queue = Queue()
        message_queue.put(ProducerAndMessage.Message("Hello"))
        message_queue.put(ProducerAndMessage.Message("from")) 
        message_queue.put(ProducerAndMessage.Message("Here"))
        senders_list[0].message_queue = message_queue 
        senders_list[0].send_simulated_messages() 
        progress_monitor = ProgressMonitor(senders_list)
        total_num_messages = 3
        result = progress_monitor.display_progress(total_num_messages)
        self.assertEqual(result,'All messages processed!')
         
if __name__ == '__main__':
    unittest.main()
