# StudyFlow — Student Planner

A desktop student-planning application built with **Python Tkinter** and **SQLite**.

## Features
- Create a local StudyFlow account and sign in.
- Add, view, edit, complete, and delete study tasks.
- Organise tasks by subject, deadline, and priority.
- View dashboard statistics and subject summaries.
- Store application data locally in SQLite.
- Passwords are stored as PBKDF2-HMAC-SHA256 hashes with individual salts.

## Requirements
- Python 3.10 or newer
- Tkinter (included with most standard Python installations)
- SQLite (included with Python)

No third-party Python packages are required.

## Run on Windows
1. Download or clone this repository.
2. Open a terminal in the repository folder.
3. Run:

   ```powershell
   python desktop_app/login.py
   ```

4. Select **Create a new account**, register, and then sign in.

## Run on macOS / Linux
From the repository root:

```bash
python3 desktop_app/login.py
```

If Tkinter is missing on Linux, install the OS package for `python3-tk`.

## Database
The app creates `desktop_app/database/studyflow.db` automatically on first launch. The generated database is intentionally excluded from Git so that local accounts and task records are not published.

## Project structure
```text
StudyFlow-Tkinter-App/
├── desktop_app/
│   ├── main.py
│   ├── login.py
│   └── database.py
├── assets/
├── documentation/
├── screenshots/
├── website/
├── README.md
├── requirements.txt
└── .gitignore
```

## Important implementation note
The current SQLite `tasks` table is not linked to individual user IDs. The login/register flow exists, but task records are shared within the local database. Do not use this version for private multi-user data without adding user ownership to the task schema and queries.

## Project status
The Python source files were checked for syntax errors. A full interactive GUI test still needs to be run on a desktop with Tkinter.
