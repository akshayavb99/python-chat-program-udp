# Basic Chat Application with sender and receiver mechanism for text only using UDP
import socket
import os
import threading
import shutil
import textwrap
import time

class userClass:
    #Defining variables to store port number to route traffic and the IP Addresses of the systems
    selfIP=""
    otherIP=""
    selfPort=0
    otherPort=0
    s=""
    terminal_width=0
    wrapper=""

    #Function to find width of terminal
    def get_terminal_width(self):
        self.terminal_width=shutil.get_terminal_size().columns
        self.wrapper=textwrap.TextWrapper(width=self.terminal_width//2)
        #print(self.terminal_width)

    #Function to find IPv4 address of local system
    def get_ip_address(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

    #Function to check if the input IPv4 address is valid using regex
    def checkIP(self,otherIPAddr):
        strIP=otherIPAddr[:]
        # check number of periods
        if strIP.count('.') != 3:
            return False

        l = list(map(str, strIP.split('.')))
        # check range of each number between periods
        for ele in l:
            if int(ele) < 0 or int(ele) > 255:
                return False

        return True

    #Function to take user input of other system's IP Address
    def get_other_ip(self):
        flag=False
        while(not flag):
            otherIPAddr=input("Enter the IP Address of other system:")
            if (self.checkIP(otherIPAddr)):
                flag=True
                return otherIPAddr
            else:
                print("Invalid IP Address!! Please enter valid IP Address")

    #Function to take port number for local system and other system
    def set_ports(self):
        self.selfPort=int(input("Enter port number of local system: "))
        self.otherPort=int(input("Enter port number for other system: "))

    #Printing sockets of both systems interacting using the Python program
    def print_data(self):
        print("Socket of local system: "+self.selfIP + ":"+str(self.selfPort))
        print("Socket of other system: " + self.otherIP + ":" + str(self.otherPort))

    def __init__(self):
        starter_strings=["----------------------",
                             "--------------------CHAT PROGRAM USING UDP---------------------",
                             "----------------------",
                             "|---------------------------------------------------------------|",
                             " ",
                             "GUIDELINES FOR PROGRAM",
                             "1. SENDER MESSAGE ON THE LEFT",
                             "2. RECEIVER MESSAGES ON THE RIGHT",
                             "3. TO EXIT OUT OF THE CHAT PROGRAM, TYPE exit"
                             ]
        self.get_terminal_width()
        print('\n'.join('{:^{}}'.format(s,self.terminal_width) for s in starter_strings))
        print()
        self.selfIP=self.get_ip_address()
        self.otherIP=self.get_other_ip()
        print()
        self.set_ports()
        print()
        #print('{:^{}}'.format("YOU CAN START MESSAGING THE OTHER SYSTEM NOW",self.terminal_width))
        #self.print_data()

        #Defining the Address Family and protocol used for communication
        protocol=socket.SOCK_DGRAM
        af=socket.AF_INET

        #Creating a socket for the program
        self.s=socket.socket(af,protocol)

        #Configuring receiver by binding the socket with local system IP Address and desired port number
        self.s.bind((self.selfIP,self.selfPort))

    def receiver(self):
        while True:
            x = self.s.recvfrom(1024)
            data=x[0].decode()
            stringMsg=self.wrapper.wrap(data)
            for i in range(len(stringMsg)):
                if (i>0):
                    if (len(stringMsg[i]) < len(stringMsg[0])):
                        stringMsg[i]=stringMsg[i]+" "*(len(stringMsg[0])-len(stringMsg[i]))
                print(stringMsg[i].rjust(self.terminal_width, " "))
            print()
            if(data == "exit"):
                print()
                print()
                endStr=["|---------------------------------------------------------------|",
                        str(self.otherIP+" has exited chat"),
                        "|---------------------------------------------------------------|"
                        ]
                print('\n'.join('{:^{}}'.format(s,self.terminal_width) for s in endStr))
                return
            time.sleep(0.2)

    def sender(self):
        while True:
            msg = input()
            #You can uncomment lines 128, and 131-136 in Windows if it has ANSI special character support enabled.
            #These lines provide text wrapping and left alignment for the sender-side messages.
            #In Linux, there is no need to check. The ANSI support is enabled, hence you can uncomment the line numbers mentioned above.
            count=len(msg)//self.terminal_width
            for i in range(count+1):
                print("\033[A                             \033[A")
            self.s.sendto(msg.encode(), (self.otherIP, self.otherPort))

            stringMsg=self.wrapper.wrap(msg)
            for i in range(len(stringMsg)):
                if (i>0):
                    if (len(stringMsg[i]) < len(stringMsg[0])):
                        stringMsg[i]=stringMsg[i]+" "*(len(stringMsg[0])-len(stringMsg[i]))
                print(stringMsg[i].ljust(self.terminal_width, " "))
            print()
            if (msg == "exit"):
                print()
                print()
                endStr=["|---------------------------------------------------------------|",
                        "The chat application is closed!!!!",
                        "|---------------------------------------------------------------|"
                        ]
                print('\n'.join('{:^{}}'.format(s,self.terminal_width) for s in endStr))
                return
            time.sleep(0.2)



if __name__ == "__main__":
    chat_app=userClass()

    #Creating threads for sender and receiver functions so that they can run simulatenously using concept of multi-threading
    sender_thread=threading.Thread(target=chat_app.sender)
    receiver_thread=threading.Thread(target=chat_app.receiver)

    #Starting both threads
    sender_thread.start()
    receiver_thread.start()

    while True:
        #If either of the threads close due to return statement, exit the program automatically
        if not sender_thread.is_alive() or not receiver_thread.is_alive():
            os._exit(1)
