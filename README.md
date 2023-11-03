# sms-simulation - SMS Alert Service Simulation

This project is designed to simulate a large-scale SMS alert service. It consists of three main components: a message producer, message senders, and a progress monitor. The simulation generates and sends a configurable number of messages to random phone numbers, simulating real-world conditions for an emergency alert service.

## Features

- **Message Producer**: Generates a specified number of messages, each containing up to 100 random characters.
- **Message Senders**: Simulates the sending process with configurable mean processing time and error rate settings. Can be scaled to multiple instances.
- **Progress Monitor**: Displays the number of messages sent, the number of failed messages, and the average time per message at regular intervals.

## Usage

To use this simulation, follow the steps below(ensure you have the latest version of Python and all libraries installed):

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the main.py script using your preferred programming language. (Command to run: python3 main.py)
4. Configure the parameters as needed for your simulation.
5. Check the progress monitor output at specified intervals.

## Configuration

Adjust the following parameters in the configuration section of the main script:

- **Number of Messages**: Configure the number of messages to be sent during the simulation.
- **Number of Senders**: Set the number of senders for the simulation.
- **Mean Processing Time**: Define the average time for processing messages for each sender.
- **Error Rate**: Set the error rate for each sender to simulate message sending failures.
- **Update Interval**: Configure the time interval for the progress monitor updates.

## Unit Testing

The project comes with comprehensive unit testing for each component. Run the unit tests to ensure the proper functioning of the simulation. They are named with 'Test' at the end to be easy to find. 

## Future 
If this simulation was actually function, I would have utilized the parameters in the Message class such as timestamp and origin phone number to stamp each message when it has been sent/by whom it was sent and whether it was successful or not and print each message sent/failed in a specific interval of time. For now, I have not done any work on those since it is still in the simulation stage. 

## References

The implementation of this project has been  aided by insights and solutions from the community at [Stack Overflow](https://stackoverflow.com/). Special thanks to the contributors for their valuable assistance.

---

By following the steps outlined in this README, you should be able to successfully simulate the SMS alert service for your desired use case. If you encounter any issues or have any suggestions, please feel free to let me know!
