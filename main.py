
import ProducerAndMessage
import Senders
import ProgressMonitor
import threading 


def sender_thread_function(sender):
    try:
        sender.send_simulated_messages()
    except KeyboardInterrupt:
        print("Sender thread interrupted.")

def progress_thread_function(progress, num_messages):
    try:
        progress.display_progress(num_messages)
    except KeyboardInterrupt:
        print("Progress thread interrupted.")
        

def get_num_senders(): #Asks user to input number of senders to prepare for 
    while True:
        try:
            num_senders = int(input("Please enter the number of senders(no default value): "))
            if num_senders > 0:
                return num_senders
            else:
                print("Number of senders must be a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")
 
            
def get_sender_configs(num_senders): #Asks user all of the configurations 
    sender_configs = []
    for i in range(num_senders):
        print(f"Configuration for Sender {i + 1} (positive integer or 'default' only): ")
        while True:
            error_rate_input = input(f"Error rate for Sender {i + 1}: ")
            mean_processing_time_input = input(f"Mean processing time for Sender {i + 1}: ")
            try:
                if error_rate_input.lower() == 'default':
                    error_rate = 'default'
                else:
                    error_rate = float(error_rate_input)

                if mean_processing_time_input.lower() == 'default':
                    mean_processing_time = 'default'
                else:
                    mean_processing_time = float(mean_processing_time_input)

                sender_configs.append({'mean_processing_time': mean_processing_time, 'error_rate': error_rate})
                break
            except ValueError:
                print("Please enter a valid float or 'default'.")
    return sender_configs

def get_update_interval(): #Asks user for the update_interval
    while True:
        try:
            update_interval_input = input("What is the update interval in seconds of the monitor (positive integer or 'default' only): ")
            if update_interval_input.lower() == 'default':
                return 'default'
            else:
                update_interval = int(update_interval_input)
                if update_interval > 0:
                    return update_interval
                else:
                    print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")

def get_num_messages(): #Asks user for number of messages to send 
    while True:
        try:
            num_messages_input = input("How many messages would you like to send? (positive integer or 'default' only): ")
            if num_messages_input.lower() == 'default':
                return 'default'
            else:
                num_messages = int(num_messages_input)
                if num_messages > 0:
                    return num_messages
                else:
                    print("Please enter a positive integer.")
        except ValueError:
            print("Please enter a valid integer.")


if __name__ == "__main__":
    try:
        
        num_messages = get_num_messages()
        update_interval = get_update_interval() #ask user for the update interval and create progress monitor object 
        num_senders = get_num_senders() #get the total number of senders
        
        sender_configs = get_sender_configs(int(num_senders)) #create sender_configs and each of the senders
        sender_list = Senders.create_senders(sender_configs)
        
        if(num_messages == 'default'):
            num_messages = 1000
        producer = ProducerAndMessage.Producer(num_messages) #create producer object 
        producer.generate_messages() #generate messages to be sent 
        
        msg_per_sender = int(num_messages) // int(num_senders) #find how many messages will be sent per sender
        remainder = int(num_messages) % int(num_senders) #the remainder if not perfectly divisible 
        
        for i in range(int(num_senders)):
            for j in range(msg_per_sender):
                message = producer.get_all_messages(
                )[i * msg_per_sender + j]
                sender_list[i].add_msg_to_queue(message) #adds messages equally to each sender 

        for i in range(remainder): #adds remainder messages equally to each sender (or as equal as possible, this makes sure the first couple senders always gets the remainder)
            message = producer.get_all_messages(
            )[int(num_messages) - remainder + i]
            sender_list[i].add_msg_to_queue(message)
       
       
        if(update_interval == 'default'):
            update_interval = 5 
        progress = ProgressMonitor.ProgressMonitor(sender_list, int(update_interval))
        
        sender_threads = [threading.Thread(target=sender_thread_function, args=(sender,)) for sender in sender_list]
        progress_thread = threading.Thread(target=progress_thread_function, args=(progress, num_messages))
    
    
        for thread in sender_threads:
            thread.start() #start each sender thread 
        progress_thread.start() #start the progress monitor thread
        
        
        for thread in sender_threads: #when finished, join each sender thread 
            thread.join()
        progress_thread.join() #join the progress_thread 

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting.")
        exit(0)
        
        