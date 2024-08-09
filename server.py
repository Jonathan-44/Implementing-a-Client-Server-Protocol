from socket import *
import sys, logging

class TCPServer:
    def __init__(self, host='127.0.0.1', port=65432):
        """
        Initializes the server instance with specified host and port.

        Sets up the server with necessary attributes for establishing a socket connection.
        Initializes a logger for the server to log various server activities and statuses.

        Parameters:
            host (str): The host address for the socket connection. Defaults to '127.0.0.1'.
            port (int): The port number for the socket connection. Defaults to 65432.

        Usage Example:
            server = TCPServer('192.168.0.1', 8080)

        Note:
            - This method should be called to create a TCPServer instance before
              starting the server with the start() method.
        """
        self.logger = logging.getLogger('SERVER')
        self.handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        self.logger.propagate = False
        self.logger.info("Initializing server...")

        # TODO: Implement any initialization code you need
        self.host = host                                  #host 
        self.port = port                                  # port
        self.server_socket = socket(AF_INET, SOCK_STREAM) #this is for TCP, AF_INET is for IPv4, SOCk_STREAM is for TCP
        self.is_running = False                           # running server 


    def start(self):
        """
        Starts the server, binding it to the specified host and port, and begins listening 
        for incoming connections.

        This method sets up a TCP/IP socket, binds it to the specified host and port, 
        and sets the server to listen for incoming connections. It also sets a 
        socket timeout of 1.0 seconds and marks the server as running.
        
        Do not attempt to accept a connection or receive any messages from the client in 
        this function.

        Exceptions:
            - socket.error: Raised if there's an issue with the socket creation or binding.

        Usage Example:
            server = TCPServer('192.168.1.10', 12345)
            server.start()

        Note:
            - Ensure that the host and port are correctly set before calling this method.
        """
        self.logger.info(f'Server is starting...')
        # TODO: Implement the server-side logic described in the method description

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)
            self.is_running = True
            self.logger.info(f'Server started and listening on {self.host}:{self.port}')

        except OSError as e:
            self.logger.error(f'Failed server start: {e}')
            self.shutdown()


    def run(self):
        """
        Handles incoming client connections and processes client requests.

        This method continuously attempts to accept new client connections. Once a client 
        is connected, it enters a loop to receive and process messages from the client, and 
        then sends back a response. The loop continues until the server is no longer running 
        or the client disconnects. If the client disconnects, the server should continue 
        attempting to accept a new client connection. The server should not shutdown until 
        the shutdown function is called or an error occurs. The outer loop should continue
        so long as self.is_running is True.

        Exceptions:
            - TimeoutError: This exception is expected and is handled by passing. This allows 
              the server to periodically check if it is still running or needs to shutdown. 
              The server could get stuck waiting to accept a connection without this timeout.
            - OSError: Raised and logged if there is a problem with the socket.
            - Exception: Generic exception to catch and log any unforeseen errors.

        Usage Example:
            server.run()

        Note:
            - The server must be started with start() before calling this method.
            - The method is blocking and will continue running until the server is shut down.
        """
        self.logger.info('Server is running...')

        # TODO: Implement the server-side logic described in the method description
        try:
            while self.is_running:
                try:
                    client_socket, client_address = self.server_socket.accept()         #here, accept a new client connection
                    self.logger.info(f"Connection established with {client_address}")
                    with client_socket:
                        while True:
                            data = client_socket.recv(1024).decode()        #received data from the client
                            if not data:
                                break  
                            response = self.process_request(data)                       
                            client_socket.sendall(response.encode())      #send the response back to the client file 
                except timeout:
                    pass        
                except OSError as e:
                    self.logger.error(f"Socket error: {e}")
                    break
                except Exception as e:
                    self.logger.error(f"Unexpected error: {e}")
                    break
        finally:
            self.shutdown()



    def shutdown(self):
        """
        Shuts down the server by stopping its operation and closing the socket.

        This method safely terminates the server's operation. It stops the server from
        running, removes the logger handler, and closes the server socket if it is open.

        The method logs the shutdown process, providing visibility into the client's
        state transitions. It's designed to be safely callable even if the socket is
        already closed or not initialized, preventing any unexpected exceptions during
        the shutdown process.

        Usage Example:
        server = TCPServer('127.0.0.1', 9385)
        server.start()
        server.run()
        # ... operations ...
        server.shutdown()

        Note:
            - Call this method to cleanly shut down the server after use or in case of an error.
        """
        self.logger.info('Server is shutting down...')

        # TODO: Implement the server-side logic described in the method description

        self.is_running = False                              
        if self.server_socket:
            try:
                self.server_socket.close()                   
                self.logger.info("Server socket closed.")
            except OSError as e:
                self.logger.error(f"Error closing server socket: {e}")

        self.logger.removeHandler(self.handler)


    def process_request(self, data):
        """
        Processes a single client request based on the received data.

        This method takes the received data string, splits it to understand the 
        requested operation and operands, and then performs the requested operation. 
        It handles addition, subtraction, division, and multiplication operations. 
        The method returns a string response that either contains the result of the 
        operation or an error message.

        Valid operations include "ADD", "SUB", "DIV", and "MUL". The operands must 
        be valid integers. Exactly two operands must be provided for every operation.

        This function must handle the following errors and return the appropriate 
        error message:
            - Exactly one operation followed by two operands must be provided. If received 
              data does not match this pattern the server should return the following 
              error message: 
              'ERROR: Invalid number of parameters. Valid format is: <OPERATION> <OPERAND1> <OPERAND2>'
            - Only the operations ADD, SUB, DIV, and MUL are supported. If an invalid operation 
              is provided the server should return the following error message:
              'ERROR: Invalid operation. Valid operations are ADD, SUB, DIV, and MUL'
            - Division by zero is not supported. If the second operand is zero the server
              should return the following error message:
              'ERROR: Division by zero error. The second operand cannot be zero.'
            - All operands must be valid integers. If an operand is not a valid integer the
              server should return the following error message:
              'ERROR: Operands must be valid integers'

        Should any other exception be raised, the server should return the following error:
        f'ERROR: {e}' where e is the exception that was raised.

        Parameters:
            data (str): The client request in the form of a string.

        Returns:
            str: The result of the operation or an error message.

        Exceptions:
            - ValueError: Raised and handled if there's an issue with parsing operands 
              (i.e. operands are not valid integers).
            - Exception: Generic exception to catch and return any unforeseen errors.

        Usage Example:
            response = process_request('ADD 5 10')

        Note:
            - Ensure that the data string is in the correct format before calling this method.
        """        
        self.logger.info(f'Processing request: {data}')
        
        # TODO: Implement the server-side logic described in the method description
        request_parts = data.strip().split()
        if len(request_parts) != 3:
            return 'ERROR: Invalid number of parameters. Valid format is: <OPERATION> <OPERAND1> <OPERAND2>'
        
        operation, operand1, operand2 = request_parts
        try:
            operand1 = int(operand1)
            operand2 = int(operand2)
        except ValueError:
            return 'ERROR: Operands must be valid integers'
        
        if operation == "ADD":
            result = operand1 + operand2
        elif operation == "SUB":
            result = operand1 - operand2
        elif operation == "DIV":
            if operand2 == 0:
                return 'ERROR: Division by zero error. The second operand cannot be zero.'
            result = operand1 / operand2
        elif operation == "MUL":
            result = operand1 * operand2
        else:
            return 'ERROR: Invalid operation. Valid operations are ADD, SUB, DIV, and MUL'
        
        return f"Result is: {result}"
        



if __name__ == '__main__':
    server = TCPServer()
    server.start()
    server.run()
