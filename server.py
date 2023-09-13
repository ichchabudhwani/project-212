import socket 
from threading import Thread
IP_ADDRESS="127.0.0.1"
PORT=8050
SERVER=None
BUFFER_SIZE=4096
import os
import time
import pygame
from pygame import mixer
import ftplib
from ftplib import FTP
from pathlib import Path
import ntpath

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

clients={}

is_dir_exists = os.path.isdir('shared_files')
print("is_dir_exists")
if(not is_dir_exists):
    os.makedirs('shared_files')

def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER



    # Sending welcome message
    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
        except:
            pass
def stop():
    global infoLabel
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('C:/Users/ichcha budhwani/Videos/Captures/'+song_selected)
    mixer.music.pause()
    infoLabel.configure(text="")
def play():
    global infoLabel
    global song_selected
    
    pygame
    mixer.init()
    mixer.music.load('C:/Users/ichcha budhwani/Videos/Captures/'+song_selected)
    mixer.music.play()
    if(song_selected!=""):
        infoLabel.configure(text="NOW PLAYING:"+song_selected)
    else:
        infoLabel.configure(text="")

def Resume():
    global song_selected
    mixer.init()
    mixer.music.load('C:/Users/ichcha budhwani/Videos/Captures/'+song_selected)
    mixer.music.play()
def Pause():
    global song_selected
    pygame
    mixer.init()
    mixer.music.load('C:/Users/ichcha budhwani/Videos/Captures/'+song_selected)
    mixer.music.pause() 

 
def handleShowList(client):
    global clients

    counter = 0
    for c in clients:
        counter +=1
        client_address = clients[c]["address"][0]
        connected_with = clients[c]["connected_with"]
        message =""
        if(connected_with):
            message = f"{counter},{c},{client_address}, connected with {connected_with},tiul,\n"
        else:
            message = f"{counter},{c},{client_address}, Available,tiul,\n"
        client.send(message.encode())
        time.sleep(1)

def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList()
    elif(message[:7] == 'resume'):
        Resume()
    elif(message[:10] =='play'):
        play()
    elif(message[:13] =='pause'):
       Pause()
    elif(message[:16] =='stop'):
        stop()
  


def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    # Sending welcome message
    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
        except:
            pass
def acceptConnections():
    global SERVER
    global clients

    while True:
        client,addr=SERVER.accept()
        client_name=client.recv(4096).decode().lower()
        clients[client_name]={
            "client"         : client,
            "address"        : addr,
            "connected_with" : "",
            "file_name"      : "",
            "file_size"      : 4096
        }
        print(f"Connection established with {client_name} : {addr}")

        thread = Thread(target = handleClient, args=(client,client_name,))
        thread.start()


def setup():
    print("\n\t\t\t\t\t\t MUSIC PLAYER\n")
    global PORT
    global IP_ADDRESS
    global SERVER

    SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(100)

    print("\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS.....")
    print("\n")
    acceptConnections()
setup_thread=Thread(target=setup)
setup_thread.start()

def ftp():
    global IP_ADDRESS
    authorizers=DummyAuthorizer()
    authorizers.add_user("lftpd","lftpd",".",perm="elradfmw")

    handler=FTPHandler
    handler.authorizer=authorizers

    ftp_server=FTPServer((IP_ADDRESS,21),handler)
    ftp_server.serve_forever()
setup_thread=Thread(target=setup)
setup_thread.start()
ftp_thread=Thread(target=ftp)
ftp_thread.start()
