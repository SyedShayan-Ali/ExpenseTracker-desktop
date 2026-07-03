import os
import sys
import customtkinter as ctk
from tkinter import ttk

from db import init_db, get_settings
from pages import (
    show_dashboard,
    show_add_transaction,
    show_transactions,
    show_settings
)


# -----------------------------
# app setup
# -----------------------------
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


init_db()

settings = get_settings()
saved_theme = settings["theme_mode"]

ctk.set_appearance_mode(saved_theme)
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Expense Tracker")
app.geometry("1200x700")
app.iconbitmap(resource_path("icon.ico"))

# -----------------------------
# Treeview style for dark modern tables
# -----------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="#1a1d24",
    foreground="white",
    fieldbackground="#1a1d24",
    borderwidth=0,
    rowheight=38,
    font=("Segoe UI", 12)
)

style.configure(
    "Treeview.Heading",
    background="#2b2f38",
    foreground="white",
    font=("Segoe UI", 13, "bold"),
    relief="flat",
    borderwidth=0,
    padding=(10, 10)
)

style.map(
    "Treeview",
    background=[("selected", "#1f6aa5")],
    foreground=[("selected", "white")]
)

style.map(
    "Treeview.Heading",
    background=[("active", "#3a3f4b")]
)


# -----------------------------
# layout frames
# -----------------------------
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.pack(side="left", fill="y")

main_area = ctk.CTkFrame(app, corner_radius=0)
main_area.pack(side="right", fill="both", expand=True)


# -----------------------------
# sidebar title
# -----------------------------
title_label = ctk.CTkLabel(sidebar, text="Expense Tracker", font=("Arial", 24, "bold"))
title_label.pack(pady=(30, 30), padx=20)


# -----------------------------
# page switching functions
# -----------------------------
def open_dashboard():
    show_dashboard(main_area)

def open_add_transaction():
    show_add_transaction(main_area)

def open_transactions():
    show_transactions(main_area)

def open_settings():
    show_settings(main_area)


# -----------------------------
# sidebar buttons
# -----------------------------
dashboard_btn = ctk.CTkButton(sidebar, text="Dashboard", command=open_dashboard, height=45)
dashboard_btn.pack(fill="x", padx=20, pady=8)

add_btn = ctk.CTkButton(sidebar, text="Add Transaction", command=open_add_transaction, height=45)
add_btn.pack(fill="x", padx=20, pady=8)

transactions_btn = ctk.CTkButton(sidebar, text="Transactions", command=open_transactions, height=45)
transactions_btn.pack(fill="x", padx=20, pady=8)

settings_btn = ctk.CTkButton(sidebar, text="Settings", command=open_settings, height=45)
settings_btn.pack(fill="x", padx=20, pady=8)


# open dashboard by default
open_dashboard()

app.mainloop()