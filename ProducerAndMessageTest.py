import unittest
from ProducerAndMessage import Producer, Message, generate_phone_number

class TestProducerAndMessage(unittest.TestCase):
    def test_generate_phone_number(self):
        phone_number = generate_phone_number()
        self.assertTrue(10 ** 9 <= phone_number <= (10 ** 10) - 1, "Generated phone number is not within the expected range.")

    def test_message_attributes(self):
        test_content = "Test message content"
        test_phone_number = generate_phone_number()
        test_message = Message(test_content)
        test_message.set_pick_up_phone_number(test_phone_number)
        test_message.set_send_timestamp(123456789)
        test_message.set_message_status("Sent")

        self.assertEqual(test_message.get_msg_content(), test_content, "Message content does not match.")
        self.assertEqual(test_message.get_pick_up_phone_number(), test_phone_number, "Sender phone number is incorrect.")
        self.assertEqual(test_message.get_send_timestamp(), 123456789, "Timestamp not set correctly.")
        self.assertEqual(test_message.get_message_status(), "Sent", "Message status not set correctly.")

    def test_producer_generate_messages(self):
        producer = Producer(num_messages=100)
        messages = producer.generate_messages()
        self.assertEqual(len(messages), 100, "Incorrect number of messages generated.")

    def test_producer_get_num_messages(self):
        producer = Producer(num_messages=100)
        self.assertEqual(producer.get_num_messages(), 100, "Incorrect default number of messages.")

    def test_producer_set_num_messages(self):
        producer = Producer()
        producer.set_num_messages(200)
        self.assertEqual(producer.get_num_messages(), 200, "Setting number of messages failed.")

    def test_producer_get_all_messages(self):
        producer = Producer(num_messages=100)
        producer.generate_messages()
        messages = producer.get_all_messages()
        self.assertEqual(len(messages), 100, "Incorrect number of messages obtained.")

if __name__ == '__main__':
    unittest.main()
