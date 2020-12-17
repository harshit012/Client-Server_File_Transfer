from uuid import uuid1
import socket
import sys
import os
import pathlib
import threading


class Model:
    _files=dict()
    _lst=""
    _user=dict()
    _loggedUsers=dict()
    def __init__(self):
        self.populateDS()

    def populateDS(self):
        x=pathlib.Path.cwd()
        Model._lst="["
        count=0
        for i in x.iterdir():
            if i.is_file():
                if count!=0: Model._lst+=","
                name=str(i.name)
                size=str(os.stat(i).st_size)
                Model._lst=Model._lst+"("+"\""+name+"\""+","+size+")"
                Model._files[name]=threading.Semaphore(5)
                count+=1
        Model._lst+="]"
        #_lst populated
        f=open("users","r")
        while True:
            line=f.readline()
            if len(line)==0: break
            tp=eval(line.strip())
            Model._user[tp[0]]=tp
        
    def listOfFiles():
        return Model._lst
    
    def verifyUser(tp):
        uname=tp[0]
        pwd=tp[1]
        if uname in Model._user:
            if Model._user[uname][1]==pwd: return True
            else: return False
        return False

    def addUser(uname):
        uid=str(uuid1())
        Model._loggedUsers[uid]=uname
        return uid

    def removeUser(uid):
        del Model._loggedUsers[uid]

    def verifyUID(uid):
         return uid in Model._loggedUsers

        

class RequestProcessor(threading.Thread):
    def __init__(self,clientSocket):
        self.clientSocket=clientSocket
        threading.Thread.__init__(self)
        self.start()
    def run(self):
        toReceive=100
        request=b''
        while len(request)<toReceive:
            by=self.clientSocket.recv(toReceive-len(request))
            request+=by
        request=request.decode("utf-8").strip()
        request=eval(request)
        uname=request[0]
        flag=Model.verifyUser(request)
        if flag==False: 
            self.clientSocket.sendall(bytes(str("(\"error\",\"Invalid username or password\")").ljust(100),"utf-8"))
        else: 
            print("user:",uname,"connected")
            uid=Model.addUser(uname)
            self.clientSocket.sendall(bytes(str("(\"No error\",\""+uid+"\""+")").ljust(100),"utf-8"))
        while flag:
            toReceive=100
            lenOfRequest=b''
            while len(lenOfRequest)<toReceive:
                by=self.clientSocket.recv(toReceive-len(lenOfRequest))    
                lenOfRequest+=by
            lenOfRequest=int(lenOfRequest.decode("utf-8").strip())
            toReceive=lenOfRequest
            request=b''
            while len(request)<toReceive:
                by=self.clientSocket.recv(toReceive-len(request))
                request+=by
            request=request.decode("utf-8").strip()
            request=eval(request)
            if Model.verifyUID(request[0])==False: 
                print("Invalid uid")
                break
            if request[1]=="logout": 
                print("user:",uname,"logout")
                Model.removeUser(uid)
                break
            elif request[1]=="dir":
                response=Model.listOfFiles()
                self.clientSocket.sendall(bytes(str(len(response)).ljust(100),"utf-8"))
                self.clientSocket.sendall(bytes(response,"utf-8"))
            elif request[1]=="get":
                fileName=str(request[2])
                if len(request)==4: fileName+="."+request[3]
                print(fileName)
                fileLocation=str(pathlib.Path.cwd())+os.path.sep+fileName
                if pathlib.Path(fileLocation).exists()==False: self.clientSocket.sendall(bytes(str("error: Invalid file name").ljust(100),"utf-8"))
                else:
                    self.clientSocket.sendall(bytes(str("File details are correct, File will be download soon").ljust(100),"utf-8"))
                    Model._files[fileName].acquire()
                    lengthOfFile=str(os.stat(fileLocation).st_size)
                    print(lengthOfFile)
                    self.clientSocket.sendall(bytes(lengthOfFile.ljust(100),"utf-8"))
                    print("length of file sent i.e:",lengthOfFile)
                    self.clientSocket.sendall(bytes(str(len(fileName)).ljust(100),"utf-8"))
                    print("Length of fileName sent i.e:",len(fileName))
                    self.clientSocket.sendall(bytes(fileName,"utf-8"))
                    print("File name sent i.e. :",fileName)
                    lengthOfFile=int(lengthOfFile)
                    ack=b''
                    while len(ack)<2:
                        by=self.clientSocket.recv(1)
                        ack+=by
                    f=open(fileLocation,"rb")
                    chunkSize=4096
                    bytesSent=0
                    while bytesSent<lengthOfFile:
                        if (lengthOfFile-bytesSent)<chunkSize: chunkSize=lengthOfFile-bytesSent
                        i=0
                        bfr=b''
                        while i<chunkSize:
                            k=f.read(1)
                            bfr+=k
                            i+=1
                        self.clientSocket.sendall(bfr)
                        ack=b''
                        while len(ack)<2:
                            by=self.clientSocket.recv(1)
                            ack+=by
                        bytesSent+=chunkSize
                        print("Bytes sent:",bytesSent)
                    Model._files[fileName].release()
                    f.close()             
        self.clientSocket.close()




t=Model()
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(("localhost",5500))
serverSocket.listen()
while True:
    print("Server is listening on port number:5500")    
    clientSocket,socketName=serverSocket.accept()
    rp=RequestProcessor(clientSocket)




