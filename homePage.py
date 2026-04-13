from Admin import AdmLogin
from voter import voterLogin
from tkinter import Frame, Tk
from ui import build_button_row, build_hero, build_option_cards, create_nav, create_surface, launch_script, prepare_root


def Home(root, frame1, frame2):
    prepare_root(root, "VoteSecure")
    create_nav(frame2, [("Home", lambda: Home(root, frame1, frame2))])
    surface = create_surface(frame1)

    build_hero(
        surface,
        "Secure Digital Voting",
        "Manage elections, register voters, and cast ballots from a calmer and more polished dashboard.",
    )
    build_button_row(
        surface,
        [
            ("Open New Window", "Accent.TButton", lambda: launch_script("homePage.py")),
        ],
    )
    build_option_cards(
        surface,
        [
            {
                "title": "Administrator Access",
                "text": "Launch the control center to start the server, register new voters, and review live vote totals.",
                "button": "Admin Login",
                "command": lambda: AdmLogin(root, frame1),
            },
            {
                "title": "Voter Portal",
                "text": "Sign in with your voter ID and password to connect to the server and cast a ballot securely.",
                "button": "Voter Login",
                "command": lambda: voterLogin(root, frame1),
                "style": "Accent.TButton",
            },
        ],
    )
def new_home():
    root = Tk()
    frame1 = Frame(root, bg="#f4efe6")
    frame2 = Frame(root, bg="#113946")
    Home(root, frame1, frame2)
    root.mainloop()


if __name__ == "__main__":
    new_home()
