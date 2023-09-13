
import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from playsound import playsound
import pygame
from pygame import mixer
import os
import time
import ftplib
from ftplib import FTP
from pathlib import Path
import ntpath



PORT  = 8080
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096
def musicWindow():

   
    print("\n\t\t\t\t MUSIC PLAYER")

    #Client GUI starts here

    
    window=Tk()

    window.title('music window')
    window.geometry("500x350")
    window.configure(bg='lightSkyBlue')

    
    
    
    global listbox
    selectLabel = Label(window, text= "Select Song", bg="lightSkyBlue",font = ("Calibri",8))
    selectLabel.place(x=2, y=1)

    listbox = Listbox(window,height = 10,width = 39,activestyle = 'dotbox', bg="lightSkyBlue",borderwidth=2,font = ("Calibri",10))
    listbox.place(x=10, y=18)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight = 1,relx = 1)
    scrollbar1.config(command = listbox.yview)

    playButton=Button(window,text="play",width=10,bd=1,bg="skyBlue", font = ("Calibri",10),command=play)
    playButton.place(x=30,y=200)

    stopButton=Button(window,text="stop",width=10,bd=1,bg="skyBlue", font = ("Calibri",10),command=stop)
    stopButton.place(x=200,y=200)

    Upload=Button(window,text="upload",width=10,bd=1,bg="skyBlue", font = ("Calibri",10),command=browseFiles)
    Upload.place(x=30,y=250)

    Download=Button(window,text="download",width=10,bd=1,bg="skyBlue", font = ("Calibri",10))
    Download.place(x=200,y=250)

    resume=Button(window,text="resume",width=10,bd=1,bg="skyBlue", font = ("Calibri",10),command=Resume)
    resume.place(x=30,y=250)

    pause=Button(window,text="pause",width=10,bd=1,bg="skyBlue", font = ("Calibri",10),command=Pause)
    pause.place(x=200,y=250)

    infoLabel = Label(window, text= "",fg= "blue", font = ("Calibri",8))
    infoLabel.place(x=4, y=200)

   

    window.mainloop()

def browseFiles():
    global listbox
    global song_counter
    global filePathLabel

    try:
        file_name= filedialog.askopenfilename()
        HOSTNAME="127.0.0.1"
        USERNAME="lftpd"
        PASSWORD="lftpd"

        ftp_server=FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding="utf-8"
        ftp_server.cwd('shared_files')
        fname=ntpath.basename(file_name)
        with open(file_name,'rb')as file:
            ftp_server.storbinary(f"STOR{fname}",file)
        ftp_server.dir()
        ftp_server.quit()

        listbox.insert(song_counter,fname)
        song_counter=song_counter+1
    except FileNotFoundError:
        print("Cancel Buttom Pressed")
def download():
        song_to_download=listbox.get(ANCHOR)
        infoLabel.configure(text="downloading"+song_to_download)
        HOSTNAME="127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD="lftpd"
        home=str(Path.home())
        download_path=home+"/Downloads"
        ftp_server=ftplib.FTP(HOSTNAME,USERNAME,PASSWORD)
        ftp_server.encoding='utf-8'
        ftp_server.cwd('shared_files')
        fname=song_to_download
        local_filename=os.path.join(download_path,fname)
        file=open(local_filename,"wb")
        ftp_server.retrbinary("RETR"+song_to_download,file.write)
        ftp_server.dir()
        file.close()
        ftp_server.quit()   
        time.sleep(1)
        if(song_selected!=""):
            infoLabel.configure(text="Now Playing"+song_selected)
        else:
            infoLabel.configure(text="")
           


def handleShowList(client):
    global listbox
    global clients
    song_counter=0
    for file in os.listdir('C:/Users/ichcha budhwani/Videos/Captures/'):
        filename=os.fsdecode(file)
        listbox.insert(song_counter,filename)
        song_counter+=1
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
    song_selected=listbox.get(ANCHOR)
    pygame
    mixer.init()
    mixer.music.load('C:/Users/ichcha budhwani/Videos/Captures/'+song_selected)
    mixer.music.play()
    if(song_selected!=""):
        infoLabel.configure(text="NOW PLAYING:"+song_selected)
    else:
        infoLabel.configure(text="")
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

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

   
    musicWindow()

setup()


