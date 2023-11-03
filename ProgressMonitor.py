import time

class ProgressMonitor:
    def __init__(self, senders_list, update_interval = 5): #Default update interval is 5 seconds 
        if update_interval < 0:
            update_interval = 5 
        self.update_interval = update_interval
        self.senders_list = senders_list
    
    def set_update_interval(self, update_interval):
        if update_interval < 0:
            update_interval = 5 
        self.update_interval = update_interval
    
    def get_update_interval(self):
        return self.update_interval 
    
    def get_senders_list(self):
        return self.senders_list

    def set_senders_list(self, senders):
        self.senders_list = senders 

    def display_progress(self, total_messages): #used to display progress (note for Athulya: , make sure to enter the total number of messages to ensure this works without causing endless loop!)
        while True:
            time.sleep(self.update_interval) #simulates processing during sleep time 
            
            total_successes = sum([sender.get_successful_messages() for sender in self.senders_list]) #gets the total number of successes across all updated senders
            total_failures = sum([sender.get_failure_messages() for sender in self.senders_list]) #gets the total number of fails across all updates senders
             
            if total_successes > 0: #calculating AVERAGE TIME per message 
                total_time = sum([sender.get_total_time() for sender in self.senders_list])
                average_time_per_message = total_time / total_successes
            else:
                average_time_per_message = 0

            print(f"Messages sent: {total_successes}, Messages failed: {total_failures}, " #printing out our updates 
                  f"Avg Time per message: {average_time_per_message:.2f} seconds")
            
            if total_successes + total_failures == total_messages:
                return "All messages processed!"
                break
                
        