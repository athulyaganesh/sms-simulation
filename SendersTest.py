import unittest
import Senders
import ProducerAndMessage

class TestSenders(unittest.TestCase):
    def test_create_senders(self):
        sender_config = [
            {'mean_processing_time': 3, 'error_rate': 7},
            {'mean_processing_time': 'default', 'error_rate': 'default'}
        ]
        senders = Senders.create_senders(sender_config)
        self.assertEqual(len(senders), 2)
        for sender in senders:
            self.assertIsInstance(sender, Senders.Sender)
            self.assertIn(sender.get_mean_processing_time(), [3, 5])
            self.assertIn(sender.get_error_rate(), [7, 5])


    def test_sender_success(self):
        sender = Senders.Sender(mean_processing_time=5, error_rate=0)
        sender.message_queue.put(ProducerAndMessage.Message("Hello"))
        sender.send_simulated_messages()
        self.assertEqual(sender.get_successful_messages(), 1)
        self.assertEqual(sender.get_failure_messages(), 0)

    
    def test_sender_failed_message(self):
        sender = Senders.Sender(mean_processing_time=1, error_rate=100)
        sender.message_queue.put(ProducerAndMessage.Message("Hello"))
        sender.send_simulated_messages()
        self.assertGreaterEqual(sender.get_failure_messages(), 0)
        
    def test_sender_with_default_values(self):
        sender =Senders.Sender()
        self.assertIn(sender.get_mean_processing_time(), [5])
        self.assertIn(sender.get_error_rate(), [5])


if __name__ == '__main__':
    unittest.main()
