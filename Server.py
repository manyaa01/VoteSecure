import socket
import threading
import dframe as df
from threading import Thread
from dframe import *
from logger import logger

lock = threading.Lock()

def client_thread(connection):

    data = connection.recv(1024)
    log = (data.decode()).split(' ')
    try:
        log[0] = int(log[0])

        if(df.verify(log[0],log[1])):
            if(df.isEligible(log[0])):
                logger.info(f"Voter authenticated — ID: {log[0]}")
                connection.send("Authenticate".encode())
            else:
                logger.warning(f"Vote already cast — ID: {log[0]}")
                connection.send("VoteCasted".encode())
        else:
            logger.warning(f"Invalid voter credentials — ID: {log[0]}")
            connection.send("InvalidVoter".encode())
            return

    except Exception as e:
        logger.error(f"Authentication error: {e}")
        connection.send("InvalidVoter".encode())
        return

    data = connection.recv(1024)
    logger.info(f"Vote received from ID: {log[0]}")
    lock.acquire()
    if(df.vote_update(data.decode(),log[0])):
        logger.info(f"Vote cast successfully — ID: {log[0]}, choice: {data.decode()}")
        connection.send("Successful".encode())
    else:
        logger.error(f"Vote update failed — ID: {log[0]}")
        connection.send("Vote Update Failed".encode())

    lock.release()
    connection.close()


def voting_Server():
    serversocket = socket.socket()
    host = socket.gethostname()
    port = 4001
    ThreadCount = 0

    try:
        serversocket.bind((host, port))
    except socket.error as e:
        logger.error(f"Failed to bind server: {e}")
        return

    logger.info(f"Server started — listening on {host}:{port}")
    serversocket.listen(10)

    while True:
        client, address = serversocket.accept()
        logger.info(f"New connection from {address}")
        client.send("Connection Established".encode())
        t = Thread(target=client_thread, args=(client,))
        t.start()
        ThreadCount += 1

    serversocket.close()

if __name__ == '__main__':
    voting_Server()
