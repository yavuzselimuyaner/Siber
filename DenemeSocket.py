
import socket
import sys


# default port for socket 
targets = [
    ('www.google.com', 80),
    ('bandit.labs.overthewire.org', 22),
    ('ftp.dlptest.com', 21),
    ('smtp.gmail.com', 25)
]



# connecting to the server
for host, port in targets:
    try: 
        host_ip = socket.gethostbyname(host)
    except socket.gaierror: 

    # this means could not resolve the host 
        print ("there was an error resolving the host")
        sys.exit() 
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print ("Socket successfully created")
    except socket.error as err: 
        print ("socket creation failed with error %s" %(err))

    try:
        s.settimeout(2)
        s.connect((host_ip, port))
        print(f"Successfully connected to port {port}")
        if port == 80:
            s.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
        data = s.recv(1024)
        with open(f"banner_raport.txt", "a") as f:
            f.write(data.decode('utf-8'))
        print(f"Received data from port {port}:\n{data.decode('utf-8')}")
    except socket.error as err:
        print(f"Connection to port {port} failed with error {err}")



print ("the socket has successfully connected to google") 