import socket
import select


def run_server():
    """
    Start a server to facilitate the chat between clients.
    The server uses a single socket to accept incoming connections
    which are then added to a list (socket_list) and are listened to
    to recieve incoming messages. Messages are then stored in a database
    and are transmitted back out to the clients.
    """

    # Define where the server is running. 127.0.0.1 is the loopback address,
    # meaning it is running on the local machine.
    host = "127.0.0.1"
    port = 5000
  
    # Create a socket for the server to listen for connecting clients
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(10)

    # Create a list to manage all of the sockets
    socket_list = []
    s = socket.socket()
    nickname_dic = {"admin": s}
    # Add the server socket to this list
    socket_list.append(server_socket)


    # Start listening for input from both the server socket and the clients
    while True:

        # Monitor all of the sockets in socket_list until something happens
        ready_to_read, ready_to_write, in_error=select.select(socket_list, [], [], 0)

        # When something happens, check each of the ready_to_read sockets
        for sock in ready_to_read:
            # A new connection request recieved
            if sock == server_socket:
                # Accept the new socket request
                sockfd, addr = server_socket.accept()
                # Add the socket to the list of sockets to monitor
                socket_list.append(sockfd)
                # Log what has happened on the server
                print ("Client (%s, %s) connected" % (addr[0],addr[1]))

            # A message from a client has been recieved
            else:
                #pass
                # YOUR CODE HERE
                # Extract the data from the socket and iterate over the socket_list
                # to send the data to each of the connected clients.
                message=sock.recv(1024).decode()
                if '/NICK' in message:
                    command = message.split(" ")[0] #extracts the /NICK command
                    nickname = message.split(" ")[1] #extracts the nickname / second parameter
                    if nickname in nickname_dic.values():
                        message='Pick a new nickname'
                        sock.send(message.encode().strip())
                    else:
                      #  print(sock)
                        nickname_dic[nickname]=sock #Puts to dic the portnumber/value and nickname/key
                        message='Nickname has been created'
                        sock.send(message.encode().strip())
                            
                elif '/WHO' in message:
                    names=''
                    for nickname,sockets in nickname_dic.items():
                        names=names+nickname+'\n'
                    sock.send(names.encode().strip())
                elif '/MSG' in message:
                    command=message.split(" ")[0] #extracts the /MSG command
                    nick=message.split(" ")[1] #extracts the nickname / second parameter
                    text=message.split(" ")[2] #extracts the text / third parameter
                    for nickname,sockets in nickname_dic.items():
                        print(nick)
                        print(nickname)
                        #find the matching nickname
                        if nickname==nick: #NO IDEA WHY THEY ARE NOT COMPARING EACH OTHER
                            message='User exist'
                            test = sockets
                            print(message)
                           # test.send(text.encode().strip())
                        else:
                            message='User does not exist'
                            #print(message)
                            sock.send(message.encode().strip())
                else:
                    for send_sock in socket_list:
                        if send_sock==sock:
                            pass
                        elif send_sock==server_socket:
                            pass
                        else:
                            send_sock.send(message.encode().strip())


     
if __name__ == '__main__':
    run_server()