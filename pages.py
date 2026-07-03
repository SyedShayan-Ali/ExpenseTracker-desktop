import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from config import EXPENSE_CATEGORIES, INCOME_CATEGORIES
from db import (
    add_transaction,
    get_all_transactions,
    delete_transaction,
    get_summary,
    get_recent_transactions,
    get_settings,
    save_settings
)


# -----------------------------
# helper function
# -----------------------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# -----------------------------
# Dashboard Page
# -----------------------------
def show_dashboard(parent_frame):
    clear_frame(parent_frame)

    settings = get_settings()
    currency = settings["currency_symbol"]
    monthly_budget = settings["monthly_budget"]

    summary = get_summary()

    budget_left = monthly_budget - summary["this_month_expense"]

    title = ctk.CTkLabel(parent_frame, text="Dashboard", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 15))

    cards_frame = ctk.CTkFrame(parent_frame)
    cards_frame.pack(padx=20, pady=10, fill="x")

    cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

    card_data = [
        ("Total Income", f"{currency} {summary['total_income']:.2f}"),
        ("Total Expense", f"{currency} {summary['total_expense']:.2f}"),
        ("Balance", f"{currency} {summary['balance']:.2f}"),
        ("This Month Expense", f"{currency} {summary['this_month_expense']:.2f}"),
        ("Monthly Budget", f"{currency} {monthly_budget:.2f}"),
        ("Budget Left", f"{currency} {budget_left:.2f}")
    ]

    for i, (label_text, value_text) in enumerate(card_data):
        row = i // 3
        col = i % 3

        card = ctk.CTkFrame(cards_frame, corner_radius=12)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(card, text=label_text, font=("Segoe UI", 16, "bold")).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=value_text, font=("Segoe UI", 18)).pack(pady=(0, 15))

    recent_label = ctk.CTkLabel(parent_frame, text="Recent Transactions", font=("Arial", 22, "bold"))
    recent_label.pack(pady=(20, 10))

    recent_frame = ctk.CTkFrame(parent_frame)
    recent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    table_container = ctk.CTkFrame(recent_frame, fg_color="transparent")
    table_container.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Type", "Amount", "Category", "Date", "Note")
    tree = ttk.Treeview(table_container, columns=columns, show="headings", height=8)

    scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    column_widths = {
        "ID": 55,
        "Type": 100,
        "Amount": 110,
        "Category": 130,
        "Date": 110,
        "Note": 260
    }

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=column_widths[col], stretch=True)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    rows = get_recent_transactions(5)
    for row in rows:
        tree.insert("", "end", values=row)


# -----------------------------
# Add Transaction Page
# -----------------------------
def show_add_transaction(parent_frame):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="Add Transaction", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 15))

    form_frame = ctk.CTkFrame(parent_frame, width=500)
    form_frame.pack(pady=10, padx=20)

    # variables
    type_var = ctk.StringVar(value="Expense")
    amount_var = ctk.StringVar()
    category_var = ctk.StringVar(value=EXPENSE_CATEGORIES[0])
    note_var = ctk.StringVar()

    # Type
    ctk.CTkLabel(form_frame, text="Type", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(20, 5))
    type_menu = ctk.CTkOptionMenu(form_frame, values=["Expense", "Income"], variable=type_var)
    type_menu.pack(fill="x", padx=20, pady=5)

    # Amount
    ctk.CTkLabel(form_frame, text="Amount", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(10, 5))
    amount_entry = ctk.CTkEntry(form_frame, textvariable=amount_var, placeholder_text="Enter amount")
    amount_entry.pack(fill="x", padx=20, pady=5)

    # Category
    ctk.CTkLabel(form_frame, text="Category", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(10, 5))
    category_menu = ctk.CTkOptionMenu(form_frame, values=EXPENSE_CATEGORIES, variable=category_var)
    category_menu.pack(fill="x", padx=20, pady=5)

    # Date
    ctk.CTkLabel(form_frame, text="Date", font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=20, pady=(10, 5))

    date_entry = DateEntry(
        form_frame,
        date_pattern="yyyy-mm-dd",
        font=("Segoe UI", 12),
        background="#1f6aa5",
        foreground="white",
        borderwidth=1
    )
    date_entry.pack(fill="x", padx=20, pady=5, ipady=6)

    # Note
    ctk.CTkLabel(form_frame, text="Note (optional)", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(10, 5))
    note_entry = ctk.CTkEntry(form_frame, textvariable=note_var, placeholder_text="Write a short note")
    note_entry.pack(fill="x", padx=20, pady=5)

    def update_categories(choice):
        if type_var.get() == "Expense":
            category_menu.configure(values=EXPENSE_CATEGORIES)
            category_var.set(EXPENSE_CATEGORIES[0])
        else:
            category_menu.configure(values=INCOME_CATEGORIES)
            category_var.set(INCOME_CATEGORIES[0])

    type_menu.configure(command=update_categories)

    def clear_form():
        type_var.set("Expense")
        amount_var.set("")
        category_menu.configure(values=EXPENSE_CATEGORIES)
        category_var.set(EXPENSE_CATEGORIES[0])
        date_entry.set_date(datetime.today())
        note_var.set("")

    def save_transaction():
        txn_type = type_var.get()
        amount_text = amount_var.get().strip()
        category = category_var.get()
        date = date_entry.get()
        note = note_var.get().strip()

        if amount_text == "":
            messagebox.showerror("Error", "Amount is required.")
            return

        try:
            amount = float(amount_text)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than 0.")
            return

        add_transaction(txn_type, amount, category, date, note)
        messagebox.showinfo("Success", "Transaction saved successfully.")
        clear_form()

    buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    save_btn = ctk.CTkButton(buttons_frame, text="Save Transaction", command=save_transaction)
    save_btn.grid(row=0, column=0, padx=10)

    clear_btn = ctk.CTkButton(buttons_frame, text="Clear", command=clear_form, fg_color="gray")
    clear_btn.grid(row=0, column=1, padx=10)


# -----------------------------
# Transactions Page
# -----------------------------
def show_transactions(parent_frame):
    clear_frame(parent_frame)

    title = ctk.CTkLabel(parent_frame, text="Transactions", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 15))

    top_frame = ctk.CTkFrame(parent_frame)
    top_frame.pack(fill="x", padx=20, pady=(0, 10))

    ctk.CTkLabel(top_frame, text="Type Filter").grid(row=0, column=0, padx=10, pady=10)

    type_filter_var = ctk.StringVar(value="All")
    type_filter = ctk.CTkOptionMenu(
        top_frame,
        values=["All", "Income", "Expense"],
        variable=type_filter_var
    )
    type_filter.grid(row=0, column=1, padx=10, pady=10)

    table_frame = ctk.CTkFrame(parent_frame)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
    table_container.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Type", "Amount", "Category", "Date", "Note")
    tree = ttk.Treeview(table_container, columns=columns, show="headings", height=14)

    scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    column_widths = {
        "ID": 55,
        "Type": 100,
        "Amount": 110,
        "Category": 130,
        "Date": 110,
        "Note": 320
    }

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=column_widths[col], stretch=True)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def load_transactions():
        for item in tree.get_children():
            tree.delete(item)

        rows = get_all_transactions()
        selected_type = type_filter_var.get()

        for row in rows:
            if selected_type == "All" or row[1] == selected_type:
                tree.insert("", "end", values=row)

    type_filter.configure(command=lambda value: load_transactions())

    def delete_selected():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Delete selected transaction?")
        if not confirm:
            return

        item = tree.item(selected[0])
        row_values = item["values"]
        transaction_id = row_values[0]

        delete_transaction(transaction_id)
        messagebox.showinfo("Deleted", "Transaction deleted successfully.")
        load_transactions()

    buttons_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    buttons_frame.pack(pady=10)

    refresh_btn = ctk.CTkButton(buttons_frame, text="Refresh", command=load_transactions)
    refresh_btn.grid(row=0, column=0, padx=10)

    delete_btn = ctk.CTkButton(buttons_frame, text="Delete Selected", command=delete_selected, fg_color="#c0392b")
    delete_btn.grid(row=0, column=1, padx=10)

    load_transactions()


# -----------------------------
# Settings Page
# -----------------------------
def show_settings(parent_frame):
    clear_frame(parent_frame)

    settings = get_settings()

    title = ctk.CTkLabel(parent_frame, text="Settings", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 15))

    form_frame = ctk.CTkFrame(parent_frame, width=500)
    form_frame.pack(pady=10, padx=20)

    budget_var = ctk.StringVar(value=str(settings["monthly_budget"]))
    currency_var = ctk.StringVar(value=settings["currency_symbol"])
    theme_var = ctk.StringVar(value=settings["theme_mode"])

    ctk.CTkLabel(form_frame, text="Monthly Budget", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(20, 5))
    budget_entry = ctk.CTkEntry(form_frame, textvariable=budget_var)
    budget_entry.pack(fill="x", padx=20, pady=5)

    ctk.CTkLabel(form_frame, text="Currency Symbol", font=("Arial", 16)).pack(anchor="w", padx=20, pady=(10, 5))
    currency_entry = ctk.CTkEntry(form_frame, textvariable=currency_var)
    currency_entry.pack(fill="x", padx=20, pady=5)

    ctk.CTkLabel(form_frame, text="Theme Mode", font=("Segoe UI", 16)).pack(anchor="w", padx=20, pady=(10, 5))

    theme_menu = ctk.CTkOptionMenu(
        form_frame,
        values=["dark", "light", "system"],
        variable=theme_var
    )
    theme_menu.pack(fill="x", padx=20, pady=5)

    def save_settings_data():
        budget_text = budget_var.get().strip()
        currency_text = currency_var.get().strip()
        theme_mode = theme_var.get().strip()

        if currency_text == "":
            messagebox.showerror("Error", "Currency symbol cannot be empty.")
            return

        if budget_text == "":
            budget_value = 0
        else:
            try:
                budget_value = float(budget_text)
            except:
                messagebox.showerror("Error", "Budget must be a number.")
                return

        save_settings(budget_value, currency_text, theme_mode)
        ctk.set_appearance_mode(theme_mode)
        messagebox.showinfo("Success", "Settings saved successfully.")

    save_btn = ctk.CTkButton(form_frame, text="Save Settings", command=save_settings_data)
    save_btn.pack(pady=20)