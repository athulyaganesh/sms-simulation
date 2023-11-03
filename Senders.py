
import queue 
import time 
import random 
import threading 

def create_senders(sender_config): #Helper function that creates senders based on providef dictionary of configurations 
    senders = []
    for current_sender in sender_config:
        mean_processing_time = current_sender['mean_processing_time']
        error_rate = current_sender['error_rate']

        if isinstance(mean_processing_time, int):
            if mean_processing_time < 0:
                mean_processing_time = 0 
        elif mean_processing_time == 'default': #default mean processing time is defined at 5 seconds
            mean_processing_time = 5
            
        if isinstance(error_rate, int):
            if error_rate < 0:
                error_rate = 0
        elif error_rate == 'default': #default error rate is defined at 5%
            error_rate = 5

        sender = Sender(
            mean_processing_time=mean_processing_time,
            error_rate=error_rate
        )
        senders.append(sender)
        
    return senders

class Sender: 
    def __init__(self, mean_processing_time = 5, error_rate = 5):
        self.mean_processing_time = mean_processing_time 
        self.error_rate = error_rate 
        self.successful_messages = 0 
        self.failure_message = 0 
        self.message_queue  = queue.Queue()
        self.total_time = 0
        self.lock = threading.Lock()
        
    def add_msg_to_queue(self, message):
        self.message_queue.put(message) 
        
    def get_mean_processing_time(self):
        return self.mean_processing_time 
    
    def get_error_rate(self):
        return self.error_rate
        
    def get_successful_messages(self):
        return self.successful_messages
    
    def get_failure_messages(self):
        return self.failure_message
    
    def get_total_time(self):
        return self.total_time 
    
    def send_simulated_messages(self):
        while not self.message_queue.empty():
            try:
                message = self.message_queue.get() #gets each message from the queue
                processing_time = max(0, random.gauss(self.mean_processing_time, 0.1)) 
                time.sleep(processing_time)#simulates processing message 
                self.total_time += processing_time #updates time 
                rad = random.random() 
                if rad < self.error_rate / 100: #simulates random failure 
                    with self.lock:
                        self.failure_message += 1
                else:
                    with self.lock: 
                        self.successful_messages += 1
            except queue.Empty:
                return "All messages processed!"
