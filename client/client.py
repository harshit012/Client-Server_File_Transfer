import socket
import os
import pathlib
import re
import sys


clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(("localhost",5500))
print("Connection established")
print("___________File downloader___________")
username=input("Enter username:")
password=input("Enter password:")
tp=f"(\"{username}\",\"{password}\")"
clientSocket.sendall(bytes(tp.ljust(100),"utf-8"))
toReceive=100
response=b''
while len(response)<toReceive:
    by=clientSocket.recv(toReceive-len(response))
    response+=by
response=response.decode("utf-8").strip()
tp=eval(response)
if tp[0]=="error":
    print("Invalid username or password")
    sys.exit();
uid=tp[1]

while True:
    command=input("tmclient>")
    lst=re.findall(r'\w+',command)
    count=0
    request="("
    request+="\""+uid+"\""
    for i in lst:
        request+=","
        request+="\""+i+"\""
    request+=")"
    if command=="quit": request=f"(\"{uid}\",\"logout\")"
    clientSocket.sendall(bytes(str(len(request)).ljust(100),"utf-8"))
    clientSocket.sendall(bytes(request,"utf-8"))
    if command=="quit": break
    elif command=="dir":
        lenOfResponse=b''
        toReceive=100
        while len(lenOfResponse)<toReceive:
            by=clientSocket.recv(toReceive-len(lenOfResponse))    
            lenOfResponse+=by
        lenOfResponse=int(lenOfResponse.decode("utf-8").strip())
        toReceive=lenOfResponse
        response=b''
        while len(response)<toReceive:
            by=clientSocket.recv(toReceive-len(response))
            response+=by
        response=response.decode("utf-8")
        lt=eval(response)
        for i in lt:
            line="File name : "+i[0].ljust(50)+"Size : "+str(i[1])
    elif command[:3]=="get":
        response=b''
        toReceive=100
        while len(response)<toReceive:
            by=clientSocket.recv(toReceive-len(response))    
            response+=by
        response=response.decode("utf-8")
        if response[:5]=="error":
            print(response)
        else:
            print("Waiting for download to begin...")
            lengthOfFile=b''
            toReceive=100
            while len(lengthOfFile)<100:
                by=clientSocket.recv(toReceive-len(lengthOfFile))
                lengthOfFile+=by
            lengthOfFile=int(lengthOfFile.decode("utf-8").strip())
            lengthOfFileName=b''
            toReceive=100
            while len(lengthOfFileName)<100:
                by=clientSocket.recv(toReceive-len(lengthOfFileName))
                lengthOfFileName+=by
            lengthOfFileName=int(lengthOfFileName.decode("utf-8").strip())
            print("Length of file name:",lengthOfFileName)
            fileName=b''
            while len(fileName)<lengthOfFileName:
                by=clientSocket.recv(lengthOfFileName-len(fileName))
                fileName+=by
            fileName=fileName.decode("utf-8")
            print("File name:",fileName)
            ack=b'56'
            clientSocket.sendall(ack)
            f=open(fileName,"wb")
            chunkSize=4096
            bytesReceived=0
            while bytesReceived<lengthOfFile:
                if (lengthOfFile-bytesReceived)<chunkSize: chunkSize=lengthOfFile-bytesReceived
                chunk=clientSocket.recv(chunkSize)
                f.write(chunk)
                clientSocket.sendall(ack)
                bytesReceived+=chunkSize
                print(f"downloading:({bytesReceived}/{lengthOfFile})")
            f.close()

clientSocket.close()

        

