'''
SMS Simulation System
Analog Devices
Author: Athulya Ganesh 

Objective:
Simulate lots of SMS alerts. Consists of the following:
    a. Producer: generates to random phone numbers
        --> Each message contains upto a 100 random characters 
        --> Num messages is configurable 
    b. Sender: receive a message fro the producer
        -->Simulate sending messages 
        --> Can configure a mean, and the messages are sent after a random period of time (around this mean)
        --> Configurable: fail rate 
    c. Progress Monitor: Displays the following stats
        --> Configurable: Updates every few seconds 
        --> The following stats need to be displayed--
            i. Num messages sent so far 
            ii. Num messages failed so far
            iii. Average time per message so far. 
            
Requirements:
    a. One instance each of : producer and progress monitor 
    b. Variable number of senders (with different mean processing time sand error rate settings) 
 
 
UNIT TEST! 
'''
from itertools import count
import time
import random
import string
import threading


def generate_phone_number():
    range_start = 10 ** 9
    range_end = (10 ** 10) - 1
    return random.randint(range_start, range_end)


def create_senders(sender_config, producer, progress_monitor):
    senders = []
    for current_sender in sender_config:
        mean_processing_time = current_sender['mean_processing_time']
        error_rate = current_sender['error_rate']

        if isinstance(mean_processing_time, int):
            pass  # Use the integer value as is
        elif mean_processing_time == 'default':
            mean_processing_time = 5
            
        if isinstance(error_rate, int):
            pass
        elif error_rate == 'default':
            error_rate = 5

        sender = Sender(
            producer=producer,
            progress_monitor=progress_monitor,
            mean_processing_time=mean_processing_time,
            error_rate=error_rate
        )
        senders.append(sender)
    return senders




class Message:
    id_iter = count()
    def __init__(self, msg_content=None):
        self.msg_content = msg_content
        self.message_id = next(self.id_iter)
        self.sender_phone_number = None
        self.timestamp_sent = None #Stays none if not sent, -1 if failed.  
        self.status = None #True = sent, False = failed 

    def get_msg_id(self):
        return self.message_id

    def get_msg_content(self):
        return self.msg_content

    def set_pick_up_phone_number(self, sender_phone_number):
        self.sender_phone_number = sender_phone_number

    def set_send_timestamp(self, timestamp):
        self.timestamp_sent = timestamp 
    
    def set_message_status(self, status):
        self.status = status 
        
        

class Producer:
    def __init__(self, num_messages=1000):
        self.num_messages = num_messages
        self.generated_messages = [] 

    def generate_messages(self):
        messages = []
        for _ in range(self.num_messages):
            message_length = random.randint(1, 100)
            message = ''.join(random.choices(string.ascii_lowercase + string.digits, k=message_length))
            m = Message(message)
            messages.append(m)
        self.generated_messages.extend(messages)
        return messages



class Sender(threading.Thread):
    def __init__(self, producer, progress_monitor, mean_processing_time, error_rate):
        super(Sender, self).__init__()
        self.phone_number = generate_phone_number()
        self.mean_processing_time = mean_processing_time
        self.error_rate = error_rate
        self.producer = producer
        self.progress_monitor = progress_monitor
        self.lock = threading.Lock()

    def send_message(self, message):
        with self.lock: 
            if self.mean_processing_time != 0:
                time.sleep(random.expovariate(1 / self.mean_processing_time))
            else:
               time.sleep(random.expovariate(1)) 
                
            if random.random() < self.error_rate / 100: 
                self.progress_monitor.update_failed_messages(message)
            else:
                self.progress_monitor.update_sent_messages(message, self.phone_number)
            self.progress_monitor.display_progress()
            
    def run(self):
        with self.lock:
            if self.producer.generated_messages:
                message = self.producer.generated_messages.pop(0)
                self.send_message(message)


class ProgressMonitor(threading.Thread):
    def __init__(self, update_interval = 5):
        super(ProgressMonitor, self).__init__()
        self.num_messages_sent = 0
        self.num_messages_failed = 0
        self.total_time = 0
        self.update_interval = update_interval
        self.lock = threading.Lock()
        self.sent_messages = {False: [], True: []}  # Messages are categorized based on display status
        self.start_time = time.time() 
        self.last_update_time = self.start_time
        self.failed_messages = {False: [], True: []}  # Failed messages categorized based on display status
        
    def update_sent_messages(self, message, phone_number):
        with self.lock:
            self.num_messages_sent += 1
            message.set_pick_up_phone_number(phone_number)
            message.timestamp_sent = time.time() 
            message.status = True
            self.sent_messages[False].append(message)  # Newly sent messages are marked as not displayed

    def update_failed_messages(self, message):
        with self.lock:
            self.num_messages_failed += 1
            message.timestamp_sent = -1 
            message.status = False 
            self.failed_messages[False].append(message)  # Newly failed messages are marked as not displayed 

    def display_progress(self):
       with self.lock:
            current_time = time.time()
            time_elapsed = current_time - self.start_time
            time_since_last_update = current_time - self.last_update_time
            print(f"Time elapsed since start:  Approximately {int(time_elapsed)} seconds")
            print(f"Time since last update: {int(time_since_last_update)} seconds")
            print(f"Number of messages sent so far: {self.num_messages_sent}")
            print(f"Number of messages failed so far: {self.num_messages_failed}")
            if self.num_messages_sent > 0:
                print(f"Average time per message so far: {self.total_time / self.num_messages_sent}\n")
            else:
                print("Average time per message so far: 0\n")
            self.last_update_time = current_time

            print("Messages Sent in Last Interval:")
            new_messages = self.sent_messages[False]  
            for message in new_messages:
                print(f"Message ID: {message.get_msg_id()}")
                print(f"Message Content: {message.get_msg_content()}")
                print(f"Sender Phone Number: {message.get_pick_phone_number()}")
                print(f"Timestamp Sent: {message.timestamp_sent}")
                print("-------------")
            print("--------------------------")

            for message in new_messages:
                self.sent_messages[True].append(message)
            self.sent_messages[False] = [] 

            print("Failed Messages in Last Interval:")
            new_failed_messages = self.failed_messages[False] 
            for message in new_failed_messages:
                print(f"Message ID: {message.get_msg_id()}")
                print(f"Message Content: {message.get_msg_content()}")
                print(f"Sender Phone Number: {message.get_pick_phone_number()}")
                print("-------------")
            print("--------------------------")

       
            for message in new_failed_messages:
                self.failed_messages[True].append(message)
            self.failed_messages[False] = [] 

    def run(self):
        while True:
            self.display_progress()
            time.sleep(self.update_interval)

if __name__ == "__main__":
    try:
        producer = Producer(1) 
        progress_monitor = ProgressMonitor(2) 
        sender_configs = [
            {'mean_processing_time': 'default', 'error_rate': 'default'}
        ]
        
        progress_monitor_thread = threading.Thread(target=progress_monitor.run)
        progress_monitor_thread.start()

        senders = create_senders(sender_configs, producer, progress_monitor)
        for sender in senders:
            sender.start() 
            sender.join()

        # Join the progress_monitor_thread to ensure it completes before the main thread exits
        progress_monitor_thread.join()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting simulation...")
        exit(0)
