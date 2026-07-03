# Expense Tracker Desktop App

A desktop Expense Tracker built with Python, CustomTkinter, and SQLite.
It helps users record expenses and income, view transaction history, manage a monthly budget, and customize the app theme.

---

## Features

* Dashboard

  * View total income, total expenses, and current balance
  * See recent transactions
  * View budget information

* Add Transaction

  * Add income or expense
  * Select category
  * Enter amount, date, and note

* Transactions

  * View all saved transactions in a clean table
  * Filter transactions by type/category
  * Browse transaction history easily

* Settings

  * Set a monthly budget
  * Change app theme
  * Save preferences inside the application

---

## Tech Stack

* Python
* CustomTkinter for the desktop UI
* Tkinter / ttk
* SQLite for local data storage

---

## Project Structure

```text
Expense Tracker/
│
├─ main.py          # main app window, layout, sidebar, app startup
├─ pages.py         # dashboard, add transaction, transactions, settings pages
├─ db.py            # database setup, insert/fetch/update functions
├─ config.py        # app constants / reusable config values
├─ icon.ico         # app icon
├─ requirements.txt # project dependencies
└─ README.md        # project documentation
```

---

## How to Run the Project from Source

### 1) Install Python

Make sure Python is installed on your system.

### 2) Install required packages

Open terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
python main.py
```

If `python` does not work on your system, use:

```bash
py main.py
```

---

## Build the EXE

The project can be packaged into a Windows executable using PyInstaller.

Example build command:

```bash
py -m PyInstaller --noconfirm --onefile --windowed --name "Expense Tracker" --icon=icon.ico --add-data "icon.ico;." main.py
```

---

## Notes

* The application stores its data locally using SQLite.
* The project was built as a beginner desktop software project to practice Python GUI development and packaging a real application.

---

## Future Improvements

Possible future upgrades:

* charts and analytics
* export to CSV / Excel
* edit existing transactions
* search transactions
* backup / restore data
* improved settings and customization

---

## Author

Created as a Python desktop project using CustomTkinter and SQLite.
