import tkinter as tk
import dframe as df
from tkinter import ttk
from ui import build_button_row, build_form, build_hero, create_surface, prepare_root, set_message

def reg_server(root,frame1,name,sex,zone,city,passw):
    if(passw=='' or passw==' '):
        Register(root, frame1, error_message="Error: missing password.")
        return -1

    vid = df.taking_data_voter(name, sex, zone, city, passw)
    prepare_root(root, "Registration Complete")
    surface = create_surface(frame1)
    build_hero(
        surface,
        "Voter Registered",
        "The new voter has been saved successfully and can now use the voter portal.",
    )
    txt = "Registered Voter with\n\n VOTER I.D. = " + str(vid)
    set_message(surface, txt, tone="success")


def Register(root,frame1,error_message=None):
    from Admin import AdminHome
    frame3 = root.winfo_children()[1]
    prepare_root(root, "Register Voter")
    surface = create_surface(frame1)
    build_button_row(
        surface,
        [("← Back", "TButton", lambda: AdminHome(root, frame1, frame3))],
    )
    build_hero(
        surface,
        "Register A New Voter",
        "Capture a voter profile and generate a fresh voter ID for the election database.",
    )

    name = tk.StringVar()
    sex = tk.StringVar()
    zone = tk.StringVar()
    city = tk.StringVar()
    password = tk.StringVar()
    build_form(
        surface,
        [
            {"label": "Name", "name": "name", "var": name},
            {"label": "Sex", "name": "sex", "var": sex, "kind": "combobox", "values": ("Male", "Female", "Transgender"), "default": "Male"},
            {"label": "Zone", "name": "zone", "var": zone},
            {"label": "City", "name": "city", "var": city},
            {"label": "Password", "name": "password", "var": password, "show": "*"},
        ],
    )
    build_button_row(
        surface,
        [
            ("Register Voter", "Primary.TButton", lambda: reg_server(root, frame1, name.get(), sex.get(), zone.get(), city.get(), password.get())),
        ],
    )
    if error_message:
        set_message(surface, error_message, tone="error")
# if __name__ == "__main__":
#         root = Tk()
#         root.geometry('500x500')
#         frame1 = Frame(root)
#         Register(root,frame1)
