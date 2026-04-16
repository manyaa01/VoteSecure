import tkinter as tk
import dframe as df
from tkinter import ttk
from ui import build_button_row, build_form, build_hero, create_surface, prepare_root, set_message


def reg_server(root, frame1, name, sex, age, zone, city, passw, password_var, error_var):
    # Clear previous error
    error_var.set("")

    if passw == '' or passw == ' ':
        password_var.set("")
        error_var.set("Error: missing password.")
        return
    if not age.isdigit() or not (18 <= int(age) <= 120):
        error_var.set("Error: age must be 18 or above.")
        return
    if len(passw) < 6:
        password_var.set("")
        error_var.set("Error: password must be at least 6 characters.")
        return
    if not any(c.isdigit() for c in passw):
        password_var.set("")
        error_var.set("Error: password must contain at least one number.")
        return
    if not any(c.isalpha() for c in passw):
        password_var.set("")
        error_var.set("Error: password must contain at least one letter.")
        return

    vid = df.taking_data_voter(name, sex, int(age), zone, city, passw)
    prepare_root(root, "Registration Complete")
    surface = create_surface(frame1)
    build_hero(
        surface,
        "Voter Registered",
        "The new voter has been saved successfully and can now use the voter portal.",
    )
    txt = "Registered Voter with\n\n VOTER I.D. = " + str(vid)
    set_message(surface, txt, tone="success")


def Register(root, frame1, error_message=None):
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
    age = tk.StringVar()
    zone = tk.StringVar()
    city = tk.StringVar()
    password = tk.StringVar()
    error_var = tk.StringVar()

    build_form(
        surface,
        [
            {"label": "Name", "name": "name", "var": name},
            {"label": "Sex", "name": "sex", "var": sex, "kind": "combobox", "values": ("Male", "Female", "Transgender"), "default": "Male"},
            {"label": "Age", "name": "age", "var": age},
            {"label": "Zone", "name": "zone", "var": zone},
            {"label": "City", "name": "city", "var": city},
            {"label": "Password", "name": "password", "var": password, "show": "*"},
        ],
    )
    tk.Label(
        surface,
        text="Password must be: at least 6 characters  •  contain a letter  •  contain a number",
        bg="#fffaf2", fg="#6a7680", font=("Helvetica", 10), justify="left"
    ).pack(anchor="w", pady=(4, 0))
    build_button_row(
        surface,
        [
            ("Register Voter", "Primary.TButton", lambda: reg_server(
                root, frame1, name.get(), sex.get(), age.get(),
                zone.get(), city.get(), password.get(), password, error_var
            )),
        ],
    )

    # Error label that updates in place
    error_label = tk.Label(surface, textvariable=error_var, bg="#fffaf2", fg="#b13d3d",
                           font=("Helvetica", 11, "bold"), justify="left", wraplength=760)
    error_label.pack(anchor="w", pady=(16, 0))
