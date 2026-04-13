import tkinter as tk
from PIL import ImageTk,Image
from tkinter import StringVar, ttk
from ui import PRIMARY, SURFACE, TEXT, build_hero, create_surface, prepare_root, set_message

def voteCast(root,frame1,vote,client_socket):

    prepare_root(root, "Vote Submitted")
    surface = create_surface(frame1)
    client_socket.send(vote.encode()) #4

    message = client_socket.recv(1024) #Success message
    print(message.decode()) #5
    message = message.decode()
    if(message=="Successful"):
        build_hero(surface, "Vote Submitted", "Your ballot has been recorded by the server.")
        set_message(surface, "Vote cast successfully.", tone="success")
    else:
        build_hero(surface, "Submission Failed", "The server did not confirm the vote. Please try again.")
        set_message(surface, "Vote cast failed. Try again.", tone="error")

    client_socket.close()



def votingPg(root,frame1,client_socket):

    prepare_root(root, "Cast Vote")
    surface = create_surface(frame1)
    build_hero(
        surface,
        "Choose Your Candidate",
        "Review each party card and click the vote button once. Your vote will be submitted immediately.",
    )

    vote = StringVar(frame1,"-1")
    options = [
        ("bjp", "BJP", "Narendra Modi", "img/bjp.png", (54, 54)),
        ("cong", "Congress", "Rahul Gandhi", "img/cong.jpg", (44, 58)),
        ("aap", "Aam Aadmi Party", "Arvind Kejriwal", "img/aap.png", (60, 44)),
        ("ss", "Shiv Sena", "Udhav Thakrey", "img/ss.png", (54, 48)),
        ("nota", "NOTA", "No candidate selected", "img/nota.jpg", (50, 38)),
    ]

    ballot = ttk.Frame(surface, style="Surface.TFrame")
    ballot.pack(fill="both", expand=True)
    frame1.image_refs = []

    for code, party, candidate, path, size in options:
        card = tk.Frame(ballot, bg=SURFACE, highlightbackground="#dccfbf", highlightthickness=1, padx=16, pady=16)
        card.pack(fill="x", pady=8)
        image = ImageTk.PhotoImage((Image.open(path)).resize(size, Image.LANCZOS))
        frame1.image_refs.append(image)
        tk.Label(card, image=image, bg=SURFACE).pack(side="left", padx=(0, 16))
        text_wrap = tk.Frame(card, bg=SURFACE)
        text_wrap.pack(side="left", fill="x", expand=True)
        tk.Label(text_wrap, text=party, bg=SURFACE, fg=PRIMARY, font=("Helvetica", 14, "bold")).pack(anchor="w")
        tk.Label(text_wrap, text=candidate, bg=SURFACE, fg=TEXT, font=("Helvetica", 11)).pack(anchor="w", pady=(4, 0))
        ttk.Button(
            card,
            text="Vote",
            style="Primary.TButton" if code != "nota" else "Accent.TButton",
            command=lambda selected=code: voteCast(root, frame1, selected, client_socket),
        ).pack(side="right")

# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         client_socket='Fail'
#         votingPg(root,frame1,client_socket)
