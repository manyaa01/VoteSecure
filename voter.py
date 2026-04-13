import tkinter as tk
import socket
from VotingPage import votingPg
from ui import build_button_row, build_form, build_hero, create_surface, prepare_root, set_message

def establish_connection():
    try:
        host = socket.gethostname()
        port = 4001
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(client_socket)
        message = client_socket.recv(1024)      #connection establishment message   #1
        if(message.decode()=="Connection Established"):
            return client_socket
        else:
            return 'Failed'
    except:
        print("Connection Failed, check if server is running...")
        return 'Failed'


def failed_return(root,frame1,client_socket,message):
    prepare_root(root, "Voter Login")
    surface = create_surface(frame1)
    build_hero(
        surface,
        "Voter Access",
        "The login flow could not continue. Please review the status message below and try again.",
    )
    set_message(surface, message + "... \nTry again.", tone="error")
    try:
        client_socket.close()
    except:
        return

def log_server(root,frame1,client_socket,voter_ID,password):
    if(not (voter_ID and password)):
        voter_ID = "0"
        password = "x"
    
    message = voter_ID + " " + password
    client_socket.send(message.encode()) #2

    message = client_socket.recv(1024) #Authenticatication message
    message = message.decode()

    if(message=="Authenticate"):
        votingPg(root, frame1, client_socket)

    elif(message=="VoteCasted"):
        message = "Vote has Already been Cast"
        failed_return(root,frame1,client_socket,message)

    elif(message=="InvalidVoter"):
        message = "Invalid Voter"
        failed_return(root,frame1,client_socket,message)

    else:
        message = "Server Error"
        failed_return(root,frame1,client_socket,message)



def voterLogin(root,frame1):
    from homePage import Home
    frame3 = root.winfo_children()[1]
    client_socket = establish_connection()
    if(client_socket == 'Failed'):
        message = "Connection failed"
        failed_return(root,frame1,client_socket,message)
        return

    prepare_root(root, "Voter Login")
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: Home(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Voter Sign In",
        "Connect to the server and verify your voter ID before moving to the ballot screen.",
    )

    voter_ID = tk.StringVar()
    password = tk.StringVar()
    build_form(
        surface,
        [
            {"label": "Voter ID", "name": "voter_id", "var": voter_ID},
            {"label": "Password", "name": "password", "var": password, "show": "*"},
        ],
    )
    build_button_row(
        surface,
        [
            ("Login", "Accent.TButton", lambda: log_server(root, frame1, client_socket, voter_ID.get(), password.get())),
        ],
    )
# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         voterLogin(root,frame1)
