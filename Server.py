from genericpath import exists
from http.client import NON_AUTHORITATIVE_INFORMATION
from pickle import NONE
import socket
from sqlite3 import connect
import threading
from urllib import request
import pyodbc
import threading

#192.168.1.20
HOST="127.0.0.1" #loopback
SERVER_PORT=65293
FORMAT="utf8"

conx=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost; database=CRYPTOCURRENCY;TRUSTED_CONNECTION=yes')
cursor=conx.cursor()

def send_information_of_an_currency(conn,nameofcurrency):
    cursor.execute("select * from CRYPTO where MA=?",nameofcurrency)
    result=cursor.fetchone()
    msg=result.TEN
    conn.sendall(msg.encode(FORMAT))
    conn.recv(1024)
    msg=result.MA;
    conn.sendall(msg.encode(FORMAT))
    conn.recv(1024)
    msg=str(result.GIA)+" USD";
    conn.sendall(msg.encode(FORMAT))
    conn.recv(1024)

def send_information_of_all_currency(conn):
    cursor.execute('''select COUNT(*) soluong
                       from CRYPTO''')
    sl=cursor.fetchone()
    conn.sendall(str((sl.soluong)).encode(FORMAT))
    conn.recv(1024)
    currencies=cursor.execute("select* from CRYPTO")
    for result in currencies:
         msg=result.TEN
         conn.sendall(msg.encode(FORMAT))
         conn.recv(1024)
         msg=result.MA;
         conn.sendall(msg.encode(FORMAT))
         conn.recv(1024)
         msg=str(result.GIA)+" USD";
         conn.sendall(msg.encode(FORMAT))
         conn.recv(1024)

def check_exist(requestofclient):
    cursor.execute('''select COUNT(*) soluong
                       from CRYPTO
                       where MA=?''',requestofclient)
    sl=cursor.fetchone()
    return int(sl.soluong)

def handlenClient(conn,addr):
   print("client address:",addr)
   print("conn:",conn.getsockname())
   print()
   msg=None
   while(True):
        msg=conn.recv(1024).decode(FORMAT)
        print("client ",addr,"says:",msg)
        a=msg.split()
        if(len(a)<2 or len(a)>2):
             if(msg=='x'):
                  msg="end"
                  conn.sendall(msg.encode(FORMAT))
                  break
             else:
                  print("Response to client",addr,": wrong request format")
                  print()
                  msg="wrong"
                  conn.sendall(msg.encode(FORMAT))
        else:
             tmp,requestofclient=map(str,msg.split())
             if(tmp!="MARKET"):
                  print("Response to client",addr,": wrong request format")
                  print()
                  msg="wrong"
                  conn.sendall(msg.encode(FORMAT))
             else:
                  if(requestofclient!="ALL"):
                      exist=check_exist(requestofclient)
                      if(exist==1):
                          msg="exist"
                          conn.sendall(msg.encode(FORMAT))
                          conn.recv(1024)
                          send_information_of_an_currency(conn,requestofclient)
                          print("Response to client",addr,": Gave information of",requestofclient)
                          print()
                      else:
                          msg="not_exist"
                          conn.sendall(msg.encode(FORMAT))
                          print("Response to client",addr,":",requestofclient,"not exist in database")
                          print()
                  else:
                      msg="all"
                      conn.sendall(msg.encode(FORMAT))
                      conn.recv(1024)
                      send_information_of_all_currency(conn)
                      print("Response to client",addr,": Gave information all currencies ")
                      print()
   print("client",addr,"finished")
   print(conn.getsockname(),"closed")
   conn.close()

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((HOST,SERVER_PORT))
server.listen()

print("SERVER SIDE")
print("server:",HOST,SERVER_PORT)
print("Waiting for client")

nClient=0
while(nClient<3):
    try:
        conn,addr=server.accept()
        Thr=threading.Thread(target=handlenClient,args=(conn,addr))
        Thr.daemon=False
        Thr.start()
    except:
        print("ERROR")
    nClient+=1
print("Server is overloaded")
print("The server will end when the clients exit")
print()
server.close()