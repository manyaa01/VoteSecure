import registerVoter as regV
import admFunc as adFunc
import tkinter as tk
from tkinter import ttk
from ui import build_button_row, build_form, build_hero, build_option_cards, create_nav, create_surface, launch_script, prepare_root, set_message


def AdminHome(root,frame1,frame3):
    from homePage import Home
    prepare_root(root, "Admin Dashboard")
    create_nav(frame3, [("Dashboard", lambda: AdminHome(root, frame1, frame3))])
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: Home(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Election Control Center",
        "Use the administrative tools below to manage voter registration, launch the local server, and inspect the count.",
    )
    build_option_cards(
        surface,
        [
            {
                "title": "Server Control",
                "text": "Start the election server before allowing voters to sign in from the voter portal.",
                "button": "Run Server",
                "command": lambda: launch_script("Server.py"),
            },
            {
                "title": "Register Voters",
                "text": "Add new voters with their demographic and location details, then issue a fresh voter ID.",
                "button": "Register Voter",
                "command": lambda: regV.Register(root, frame1),
                "style": "Accent.TButton",
            },
            {
                "title": "Live Results",
                "text": "Open the results view to see current vote totals for every party and the NOTA option.",
                "button": "Show Votes",
                "command": lambda: adFunc.showVotes(root, frame1),
            },
            {
                "title": "Reset Election",
                "text": "Reset all vote counts to zero and allow all voters to cast their ballot again for a fresh election round.",
                "button": "Reset Election",
                "command": lambda: adFunc.resetAll(root, frame1),
                "style": "Accent.TButton",
            },
        ],
    )
def log_admin(root,frame1,admin_ID,password):

    if(admin_ID=="Admin" and password=="admin"):
        frame3 = root.winfo_children()[1]
        AdminHome(root, frame1, frame3)
    else:
        AdmLogin(root, frame1, error_message="Either ID or password is incorrect.")


def AdmLogin(root,frame1,error_message=None):
    from homePage import Home
    frame3 = root.winfo_children()[1]
    prepare_root(root, "Admin Login")
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: Home(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Administrator Sign In",
        "Enter the admin credentials to access registration, server controls, and the vote count dashboard.",
    )

    admin_ID = tk.StringVar()
    password = tk.StringVar()
    form, _ = build_form(
        surface,
        [
            {"label": "Admin ID", "name": "admin_id", "var": admin_ID},
            {"label": "Password", "name": "password", "var": password, "show": "*"},
        ],
    )
    build_button_row(
        surface,
        [
            ("Login", "Primary.TButton", lambda: log_admin(root, frame1, admin_ID.get(), password.get())),
        ],
    )
    if error_message:
        set_message(surface, error_message, tone="error")
    ttk.Label(form, text="Default demo credentials: Admin / admin", style="Subheading.TLabel").grid(
        row=2, column=0, columnspan=2, sticky="w", pady=(6, 0)
    )
# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         frame3 = Frame(root)
#         AdminHome(root,frame1,frame3)
