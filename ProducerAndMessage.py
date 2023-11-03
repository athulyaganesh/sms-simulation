
import random 
from itertools import count
import queue
import string 

def generate_phone_number(): #function to generate random 10 digit phone numbers 
    range_start = 10 ** 9
    range_end = (10 ** 10) - 1
    return random.randint(range_start, range_end)


class Message: #class to store information about each message that is sent including content, ID, the sender phone number etc. 
    id_iter = count()
    def __init__(self, msg_content=None):
        self.msg_content = msg_content
        self.message_id = next(self.id_iter)
        self.sender_phone_number = None 
        self.timestamp_sent = None #If set to None has not been sent yet, -1 = failure message, Any other value gives us the timestamp 
        self.status = None #If set to none has not been sent yet, False = failure, True = sent successfully 

    def get_msg_id(self):
        return self.message_id

    def get_msg_content(self):
        return self.msg_content
    
    def set_msg_content(self, content):
        return self.msg_content 

    def set_pick_up_phone_number(self, sender_phone_number):
        self.sender_phone_number = sender_phone_number
    
    def get_pick_up_phone_number(self):
        return self.sender_phone_number 

    def set_send_timestamp(self, timestamp):
        self.timestamp_sent = timestamp 
    
    def get_send_timestamp(self):
        return self.timestamp_sent 
    
    def set_message_status(self, status):
        self.status = status 
    
    def get_message_status(self):
        return self.status 


class Producer:
    def __init__(self, num_messages=1000): #default is a 1000 messages 
        if num_messages < 0:
            num_messages = 0 
        self.num_messages = num_messages
        self.generated_messages = []  #create a queue for generated messages 

    def generate_messages(self):
        for _ in range(self.num_messages): #randomly generate strings from length 1 to 100 
            message_length = random.randint(1, 100)
            message = ''.join(random.choices(string.ascii_lowercase + string.digits, k=message_length))
            m = Message(message)
            self.generated_messages.append(m)
        return self.generated_messages

    def get_num_messages(self):
        return self.num_messages
    
    def set_num_messages(self, num_messages): 
        if num_messages < 0:
            num_messages = 0 
        self.num_messages = num_messages
    
    def get_all_messages(self):
        return self.generated_messages