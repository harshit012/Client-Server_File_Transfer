# Client-Server_File_downloader
This is a basic TCP/IP based client-server network application which allow users to download the files stored on the server. The server is multithreaded, So It can process multiple request simultaneously.

## Features
* Server is multithreaded.
* The user has to provide his/her credentials to download files.
* One file can be downloaded by maximum 5 users.
* Works on TCP/IP protocol.
* Easy to use & faster downloading.

## System Requirement
* Python 3.6 or greater
* Modules required :Threading , Socket

## How To use:

### Step 1 
Download client.py & server.py 
1) There is file named users in client folder, Which contains all the necessary information about users, you can add/edit/delete user according to specified format i.e. in tuple form. technically the details of all the users should be encrypted but this is basic application ,I did not do it.
2) Add some random files in server folder, the files can be audio,video,image etc. you can even add the file of size in TBs.
3) Run server.py , If you are windows user then firewall asks for some permission. 
4) Now the server is listening on port 5050. 
5) Run client.py
6) Authentication is performed at client's end. you have to enter correct credential to proceed further.
7) After successful login, Type "dir" command and press enter.
8) It will display all the necessary information about the files at server end.
9) If you want to download a file, then type "get <filename>" 
10) Download will begin soon , If more than 5 client are downloading the same file, then you have to wait until the one of the user has finished the downloading.
11) If you want to quit the application, type "quit" , The request for logout will be sent to server & you will be logout and then the application ends at client side.
