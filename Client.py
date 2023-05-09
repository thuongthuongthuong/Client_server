from pickle import NONE
import socket


HOST="127.0.0.1" #loopback
SERVER_PORT=65293
FORMAT="utf8"

def receive_information_of_an_currency(conn):
    msg=None
    msg=conn.recv(1024).decode(FORMAT)
    print("                   ","Name of currency:",msg)
    conn.sendall(msg.encode(FORMAT))
    msg=conn.recv(1024).decode(FORMAT)
    print("                   ","Short name for cryptocurrency:",msg)
    conn.sendall(msg.encode(FORMAT))
    msg=conn.recv(1024).decode(FORMAT)
    print("                   ","Price of cryptocurrency:",msg)
    conn.sendall(msg.encode(FORMAT))

def receive_information_of_all_currency(conn):
    n=conn.recv(1024).decode(FORMAT)
    conn.sendall(str(n).encode(FORMAT))
    msg=None
    for i in range(int(n)):
        msg=conn.recv(1024).decode(FORMAT)
        print("                   ","Name of currency:",msg)
        conn.sendall(msg.encode(FORMAT))
        msg=conn.recv(1024).decode(FORMAT)
        print("                   ","Short name for cryptocurrency:",msg)
        conn.sendall(msg.encode(FORMAT))
        msg=conn.recv(1024).decode(FORMAT)
        print("                   ","Price of cryptocurrency:",msg)
        conn.sendall(msg.encode(FORMAT))
        print()

client =socket.socket(socket.AF_INET,socket.SOCK_STREAM)

print("CLIENT SIDE")

try:
    client.connect((HOST,SERVER_PORT))
    print("client address:",client.getsockname())
    print()
    msg=None
    msg1=None
    while(True):
        msg=input('talk: ')
        client.sendall(msg.encode(FORMAT))
        msg1=client.recv(1024).decode(FORMAT)
        if(msg1=="exist"):
            client.sendall(msg1.encode(FORMAT))
            tmp,requestofclient=map(str,msg.split())
            print("Server respone: Information of ",requestofclient)
            print()
            receive_information_of_an_currency(client)
            print()
        elif msg1=="all":
            client.sendall(msg.encode(FORMAT))
            print("Server respone: Information of all curencies")
            print()
            receive_information_of_all_currency(client)
            print()
        elif msg1=="end":
            break
        elif msg1=="wrong":
            print("Server respone: wrong request format")
        elif msg1=="not_exist":
            tmp,requestofclient=map(str,msg.split())
            print("Server respone: ",requestofclient,"not exist in database")
except:
    print("error")
print("end")
