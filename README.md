# Client-Server_File_downloader
This is a basic TCP/IP based client-server network application which allow users to download the files stored on the server. The server is multithreaded, So It can process multiple request simultaneously.

The application will be useful if all the machines are connected to the same local network.

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

**Step 1** : Download zip file & extract it.

**Step 2** : Add some random files in server folder, The files can be audio,video,image etc. you can even add the files of size in TBs.

There is file named users in server folder, Which contains all the necessary information about the users, you can add/edit/delete user according to the specified format i.e. in the form of tuple. The details of all the users should be encrypted but this is basic application, so I have not done the encryption.


**Step 3** : Run server.py , If you are windows user then firewall may ask for some permission. 

Now the server is listening on port 5050. 

**Step 4** : Run client.py
Authentication is performed at client's end. you have to enter correct credential to proceed further.

**Step 5** : After successful login, Type "dir" command and press enter. It will display all the information about the files at server end.

If you want to download a file, then type "get <filename>" 
Download will begin soon , If more than 5 client are already downloading the same file, Then you have to wait until the anyone of the user five users have finished the downloading

If you want to quit the application, type "quit" , The request for logout will be sent to server & you will be logout and then the application ends at client side.
