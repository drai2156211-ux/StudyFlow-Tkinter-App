import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from database import StudyFlowDatabase

# StudyFlow 3.0 — Light editorial dashboard
BG = "#F4F6FB"
WHITE = "#FFFFFF"
NAVY = "#17233B"
NAVY_2 = "#22314F"
TEXT = "#17233B"
MUTED = "#77839A"
LINE = "#E6EAF2"
PURPLE = "#6D4AFF"
PURPLE_SOFT = "#F0ECFF"
BLUE = "#3977E8"
BLUE_SOFT = "#EAF2FF"
GREEN = "#159B72"
GREEN_SOFT = "#E6F7F1"
AMBER = "#C88718"
AMBER_SOFT = "#FFF4DE"
RED = "#D94D65"
RED_SOFT = "#FDECEF"


class StudyFlowApp:
    def __init__(self, root):
        self.root = root
        self.db = StudyFlowDatabase()
        self.root.title("StudyFlow | Student Workspace")
        self.root.geometry("1420x900")
        self.root.minsize(1120, 720)
        self.root.configure(bg=BG)
        self.selected_task_id = None
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All tasks")
        self._styles()
        self._shell()
        self.show_dashboard()

    def _styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("SF.Treeview", background=WHITE, fieldbackground=WHITE,
                    foreground=TEXT, rowheight=44, borderwidth=0,
                    font=("Segoe UI", 10))
        s.configure("SF.Treeview.Heading", background="#F0F3F9",
                    foreground=MUTED, relief="flat", borderwidth=0,
                    font=("Segoe UI", 9, "bold"), padding=(12, 13))
        s.map("SF.Treeview", background=[("selected", PURPLE_SOFT)],
              foreground=[("selected", TEXT)])
        s.configure("SF.Vertical.TScrollbar", background="#DDE3EF",
                    troughcolor=WHITE, bordercolor=WHITE, arrowcolor=MUTED)
        s.configure("SF.TCombobox", fieldbackground="#F7F8FC",
                    background="#F7F8FC", foreground=TEXT,
                    arrowcolor=MUTED, padding=9, bordercolor=LINE)
        s.map("SF.TCombobox", fieldbackground=[("readonly", "#F7F8FC")],
              foreground=[("readonly", TEXT)])

    def _shell(self):
        self.sidebar = tk.Frame(self.root, bg=NAVY, width=248)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=NAVY)
        brand.pack(fill="x", padx=25, pady=(30, 44))
        mark = tk.Canvas(brand, width=36, height=36, bg=NAVY,
                         highlightthickness=0)
        mark.pack(side="left")
        mark.create_oval(3, 3, 33, 33, fill=PURPLE, outline="")
        mark.create_text(18, 18, text="S", fill=WHITE,
                         font=("Segoe UI", 16, "bold"))
        tk.Label(brand, text="StudyFlow", bg=NAVY, fg=WHITE,
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=10)

        tk.Label(self.sidebar, text="WORKSPACE", bg=NAVY, fg="#8190AA",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=27, pady=(0, 12))
        self.nav = {}
        items = [
            ("Overview", "▦", self.show_dashboard),
            ("My tasks", "✓", self.show_tasks),
            ("Subjects", "▤", self.show_subjects),
            ("Settings", "⚙", self.show_settings),
        ]
        for name, symbol, fn in items:
            b = tk.Button(self.sidebar, text=f"   {symbol}     {name}",
                          command=fn, anchor="w", bg=NAVY, fg="#B8C4D8",
                          activebackground=NAVY_2, activeforeground=WHITE,
                          bd=0, relief="flat", padx=14, pady=15,
                          font=("Segoe UI", 10, "bold"), cursor="hand2")
            b.pack(fill="x", padx=13, pady=3)
            self.nav[name] = b

        spacer = tk.Frame(self.sidebar, bg=NAVY)
        spacer.pack(fill="both", expand=True)
        side_note = tk.Frame(self.sidebar, bg=NAVY_2, padx=14, pady=14)
        side_note.pack(fill="x", padx=15, pady=18)
        tk.Label(side_note, text="YOUR STUDY SPACE", bg=NAVY_2, fg="#AEBBD0",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(side_note, text="Plan with purpose.\nLearn at your pace.",
                 bg=NAVY_2, fg=WHITE, justify="left",
                 font=("Segoe UI", 10), pady=8).pack(anchor="w")
        tk.Label(self.sidebar, text="STUDYFLOW  •  2026", bg=NAVY,
                 fg="#72819A", font=("Segoe UI", 8)).pack(pady=(0, 20))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

    def _activate(self, name):
        for key, button in self.nav.items():
            active = key == name
            button.configure(bg="#332B68" if active else NAVY,
                             fg=WHITE if active else "#B8C4D8")

    def _clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    def _header(self, section, title, subtitle):
        self._activate(section)
        top = tk.Frame(self.main, bg=BG)
        top.pack(fill="x", padx=38, pady=(27, 18))
        left = tk.Frame(top, bg=BG)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=section.upper(), bg=BG, fg=PURPLE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(left, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 25, "bold")).pack(anchor="w", pady=(5, 2))
        tk.Label(left, text=subtitle, bg=BG, fg=MUTED,
                 font=("Segoe UI", 10)).pack(anchor="w")
        tk.Label(top, text=datetime.now().strftime("%a, %d %b %Y"),
                 bg=BG, fg=MUTED, font=("Segoe UI", 9)).pack(side="right", pady=12)

    def _card(self, parent, padx=18, pady=16):
        return tk.Frame(parent, bg=WHITE, padx=padx, pady=pady,
                        highlightthickness=1, highlightbackground=LINE)

    def _btn(self, parent, text, command, primary=True):
        bg = PURPLE if primary else WHITE
        fg = WHITE if primary else TEXT
        return tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                         activebackground="#5938E8" if primary else "#F1F3F8",
                         activeforeground=fg, bd=0, relief="flat",
                         font=("Segoe UI", 9, "bold"), padx=16, pady=10,
                         cursor="hand2",
                         highlightthickness=1 if not primary else 0,
                         highlightbackground=LINE)

    def _tasks(self):
        return self.db.get_tasks()

    def _stats(self):
        return self.db.get_statistics()

    def _section_title(self, parent, title, action=None, command=None):
        row = tk.Frame(parent, bg=BG)
        row.pack(fill="x", pady=(0, 10))
        tk.Label(row, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI", 13, "bold")).pack(side="left")
        if action:
            tk.Button(row, text=action, command=command, bg=BG, fg=PURPLE,
                      activebackground=BG, activeforeground=PURPLE,
                      bd=0, font=("Segoe UI", 9, "bold"),
                      cursor="hand2").pack(side="right")

    # ---------------- DASHBOARD ----------------

    def show_dashboard(self):
        self._clear()
        self._header("Overview", "Your study day, organised.",
                     "A simple view of what is done and what deserves your attention.")
        total, pending, completed, subjects = self._stats()
        rows = self._tasks()

        # Hero strip
        hero = tk.Frame(self.main, bg=NAVY_2, padx=25, pady=21)
        hero.pack(fill="x", padx=38, pady=(0, 18))
        hero_left = tk.Frame(hero, bg=NAVY_2)
        hero_left.pack(side="left", fill="x", expand=True)
        tk.Label(hero_left, text="SMALL STEPS. REAL PROGRESS.", bg=NAVY_2,
                 fg="#BBAEFF", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(hero_left, text="Make room for focused learning.",
                 bg=NAVY_2, fg=WHITE, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(5, 3))
        tk.Label(hero_left, text="Add your next assignment and keep momentum going.",
                 bg=NAVY_2, fg="#C5D0E2", font=("Segoe UI", 9)).pack(anchor="w")
        self._btn(hero, "+  New task", self.add_task).pack(side="right", padx=(10, 0))

        # Metric cards
        metric_row = tk.Frame(self.main, bg=BG)
        metric_row.pack(fill="x", padx=32, pady=(0, 19))
        metrics = [
            ("Tasks in planner", total, "All your activities", PURPLE, PURPLE_SOFT, "▦"),
            ("To do", pending, "Waiting for your focus", AMBER, AMBER_SOFT, "◷"),
            ("Completed", completed, "Progress made so far", GREEN, GREEN_SOFT, "✓"),
            ("Subjects", subjects, "Your learning areas", BLUE, BLUE_SOFT, "▤"),
        ]
        for i, (label, value, note, accent, tint, symbol) in enumerate(metrics):
            metric_row.grid_columnconfigure(i, weight=1)
            card = self._card(metric_row, 15, 14)
            card.grid(row=0, column=i, padx=6, sticky="nsew")
            head = tk.Frame(card, bg=WHITE)
            head.pack(fill="x")
            tk.Label(head, text=label, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9, "bold")).pack(side="left")
            tk.Label(head, text=symbol, bg=tint, fg=accent,
                     font=("Segoe UI", 12, "bold"), padx=7, pady=4).pack(side="right")
            tk.Label(card, text=str(value), bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 26, "bold")).pack(anchor="w", pady=(10, 0))
            tk.Label(card, text=note, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w", pady=(1, 0))

        # Progress + deadlines two-column layout
        lower = tk.Frame(self.main, bg=BG)
        lower.pack(fill="x", padx=38, pady=(0, 18))
        lower.grid_columnconfigure(0, weight=3)
        lower.grid_columnconfigure(1, weight=2)

        progress = self._card(lower, 19, 17)
        progress.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        tk.Label(progress, text="Your progress", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(progress, text="A quick snapshot of your task completion.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 13))
        pct = int((completed / total) * 100) if total else 0
        bar_bg = tk.Frame(progress, bg="#EDF0F6", height=12)
        bar_bg.pack(fill="x", pady=(0, 8))
        bar_bg.pack_propagate(False)
        if pct:
            tk.Frame(bar_bg, bg=PURPLE, width=max(8, int(450 * pct / 100))).pack(side="left", fill="y")
        foot = tk.Frame(progress, bg=WHITE)
        foot.pack(fill="x")
        tk.Label(foot, text=f"{pct}% completed", bg=WHITE, fg=PURPLE,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(foot, text=f"{completed} of {total} tasks", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8)).pack(side="right")

        deadlines = self._card(lower, 19, 17)
        deadlines.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        tk.Label(deadlines, text="Coming up", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w")
        tk.Label(deadlines, text="Your next deadlines", bg=WHITE, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 9))
        upcoming = [r for r in rows if r[5] != "Completed"]
        upcoming.sort(key=lambda r: r[3])
        if not upcoming:
            tk.Label(deadlines, text="Nothing due right now.\nAdd a task to plan ahead.",
                     bg=WHITE, fg=MUTED, justify="left",
                     font=("Segoe UI", 9)).pack(anchor="w", pady=8)
        else:
            for r in upcoming[:3]:
                line = tk.Frame(deadlines, bg=WHITE)
                line.pack(fill="x", pady=5)
                tk.Label(line, text="•", bg=WHITE, fg=PURPLE,
                         font=("Segoe UI", 14, "bold")).pack(side="left")
                info = tk.Frame(line, bg=WHITE)
                info.pack(side="left", padx=7, fill="x", expand=True)
                tk.Label(info, text=r[1], bg=WHITE, fg=TEXT,
                         font=("Segoe UI", 9, "bold")).pack(anchor="w")
                tk.Label(info, text=f"{r[2]}  ·  {r[3]}", bg=WHITE, fg=MUTED,
                         font=("Segoe UI", 8)).pack(anchor="w")

        # Recent activity table
        section = tk.Frame(self.main, bg=BG)
        section.pack(fill="both", expand=True, padx=38, pady=(0, 24))
        self._section_title(section, "Recent tasks", "See all tasks →", self.show_tasks)
        recent = rows[:5]
        if recent:
            panel = self._card(section, 8, 8)
            panel.pack(fill="both", expand=True)
            self._make_table(panel, recent, height=min(5, len(recent)))
        else:
            empty = self._card(section, 20, 18)
            empty.pack(fill="x")
            tk.Label(empty, text="Your task list is waiting for its first entry.",
                     bg=WHITE, fg=TEXT, font=("Segoe UI", 11, "bold")).pack(anchor="w")
            tk.Label(empty, text="Create a task to start tracking your assignments and deadlines.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 12))
            self._btn(empty, "+  Create first task", self.add_task).pack(anchor="w")

    # ---------------- TABLE / TASKS ----------------

    def _make_table(self, parent, rows, height=10, expand=False):
        wrap = tk.Frame(parent, bg=WHITE)
        wrap.pack(fill="both", expand=expand)
        cols = ("id", "title", "subject", "deadline", "priority", "status")
        labels = {"id": "ID", "title": "TASK", "subject": "SUBJECT",
                  "deadline": "DUE DATE", "priority": "PRIORITY", "status": "STATUS"}
        widths = {"id": 50, "title": 260, "subject": 150,
                  "deadline": 125, "priority": 100, "status": 110}
        tree = ttk.Treeview(wrap, columns=cols, show="headings",
                            height=height, style="SF.Treeview")
        for col in cols:
            tree.heading(col, text=labels[col])
            tree.column(col, width=widths[col],
                        anchor="center" if col in ("id", "priority", "status") else "w",
                        stretch=True)
        scroll = ttk.Scrollbar(wrap, orient="vertical",
                               command=tree.yview, style="SF.Vertical.TScrollbar")
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        if len(rows) > height:
            scroll.pack(side="right", fill="y")
        for row in rows:
            tree.insert("", "end", values=row)
        return tree

    def show_tasks(self):
        self._clear()
        self._header("My tasks", "Keep every assignment moving.",
                     "Search, filter and update your academic workload.")
        toolbar = tk.Frame(self.main, bg=BG)
        toolbar.pack(fill="x", padx=38, pady=(0, 13))
        search = tk.Entry(toolbar, textvariable=self.search_var, bg=WHITE, fg=TEXT,
                          insertbackground=TEXT, relief="flat", font=("Segoe UI", 10),
                          highlightthickness=1, highlightbackground=LINE, width=25)
        search.pack(side="left", ipady=10, padx=(0, 9))
        search.bind("<Return>", lambda _e: self._refresh())
        combo = ttk.Combobox(toolbar, textvariable=self.filter_var,
                             values=["All tasks", "Pending", "Completed"],
                             state="readonly", width=14, style="SF.TCombobox")
        combo.pack(side="left", ipady=4)
        combo.bind("<<ComboboxSelected>>", lambda _e: self._refresh())
        self._btn(toolbar, "Search", self._refresh, primary=False).pack(side="left", padx=7)
        self._btn(toolbar, "+ Add task", self.add_task).pack(side="right")
        self._btn(toolbar, "Edit", self.edit_task, primary=False).pack(side="right", padx=6)
        self._btn(toolbar, "Complete", self.complete_task, primary=False).pack(side="right", padx=6)
        self._btn(toolbar, "Delete", self.delete_task, primary=False).pack(side="right", padx=6)

        panel = self._card(self.main, 9, 9)
        panel.pack(fill="both", expand=True, padx=38, pady=(0, 10))
        self.task_table = self._make_table(panel, self._filtered(), height=13, expand=True)
        self.task_table.bind("<<TreeviewSelect>>", self._on_select)
        self.task_table.bind("<Double-1>", lambda _e: self.edit_task())
        tk.Label(self.main, text="Select a row to edit, complete or delete a task.",
                 bg=BG, fg=MUTED, font=("Segoe UI", 8)).pack(anchor="w", padx=40, pady=(0, 15))

    def _filtered(self):
        rows = self._tasks()
        q = self.search_var.get().strip().lower()
        f = self.filter_var.get()
        out = []
        for row in rows:
            if f in ("Pending", "Completed") and row[5] != f:
                continue
            if q and q not in " ".join(str(x) for x in row[1:]).lower():
                continue
            out.append(row)
        return out

    def _refresh(self):
        if not hasattr(self, "task_table") or not self.task_table.winfo_exists():
            return
        for item in self.task_table.get_children():
            self.task_table.delete(item)
        for row in self._filtered():
            self.task_table.insert("", "end", values=row)

    def _on_select(self, _event=None):
        selected = self.task_table.selection()
        self.selected_task_id = int(self.task_table.item(selected[0], "values")[0]) if selected else None

    # ---------------- ADD / EDIT ----------------

    def _task_form(self, title, row=None):
        win = tk.Toplevel(self.root)
        win.title("StudyFlow | " + title)
        win.geometry("520x610")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        panel = tk.Frame(win, bg=WHITE, padx=30, pady=26,
                         highlightthickness=1, highlightbackground=LINE)
        panel.pack(fill="both", expand=True, padx=18, pady=18)
        tk.Label(panel, text=title, bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(panel, text="Add the details below. You can update them later.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 18))

        defaults = (row[1], row[2], row[3], row[4]) if row else ("", "", "", "Medium")
        entries = {}
        for label, value in zip(("Task title", "Subject", "Deadline (YYYY-MM-DD)"), defaults[:3]):
            tk.Label(panel, text=label, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(9, 5))
            e = tk.Entry(panel, bg="#F7F8FC", fg=TEXT, insertbackground=TEXT,
                         relief="flat", font=("Segoe UI", 10),
                         highlightthickness=1, highlightbackground=LINE)
            e.pack(fill="x", ipady=10)
            e.insert(0, str(value))
            entries[label] = e
        tk.Label(panel, text="Priority", bg=WHITE, fg=TEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(14, 5))
        priority = ttk.Combobox(panel, values=["High", "Medium", "Low"],
                                 state="readonly", style="SF.TCombobox")
        priority.set(defaults[3])
        priority.pack(fill="x", ipady=5)

        def save():
            task = entries["Task title"].get().strip()
            subject = entries["Subject"].get().strip()
            due = entries["Deadline (YYYY-MM-DD)"].get().strip()
            if not task or not subject or not due:
                messagebox.showwarning("Missing details", "Please fill in all fields.", parent=win)
                return
            try:
                datetime.strptime(due, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid date", "Use YYYY-MM-DD format.", parent=win)
                return
            if row:
                self.db.update_task(row[0], task, subject, due, priority.get())
            else:
                self.db.add_task(task, subject, due, priority.get())
            win.destroy()
            self.selected_task_id = None
            self.show_tasks() if row else self.show_dashboard()

        self._btn(panel, "Save task", save).pack(fill="x", pady=(24, 0), ipady=3)

    def add_task(self):
        self._task_form("Create a task")

    def edit_task(self):
        if not self.selected_task_id:
            messagebox.showinfo("Select a task", "Select a task first.")
            return
        row = next((r for r in self._tasks() if r[0] == self.selected_task_id), None)
        if row:
            self._task_form("Edit task", row)

    def complete_task(self):
        if not self.selected_task_id:
            messagebox.showinfo("Select a task", "Select a task first.")
            return
        self.db.complete_task(self.selected_task_id)
        self.selected_task_id = None
        self.show_tasks()

    def delete_task(self):
        if not self.selected_task_id:
            messagebox.showinfo("Select a task", "Select a task first.")
            return
        if messagebox.askyesno("Delete task", "Delete the selected task?"):
            self.db.delete_task(self.selected_task_id)
            self.selected_task_id = None
            self.show_tasks()

    # ---------------- SUBJECTS / SETTINGS ----------------

    def show_subjects(self):
        self._clear()
        self._header("Subjects", "Your learning areas.",
                     "Subjects are collected automatically from the tasks you add.")
        counts = {}
        for row in self._tasks():
            counts[row[2]] = counts.get(row[2], 0) + 1
        body = tk.Frame(self.main, bg=BG)
        body.pack(fill="both", expand=True, padx=38)
        if not counts:
            panel = self._card(body, 22, 22)
            panel.pack(fill="x")
            tk.Label(panel, text="No subjects yet", bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 13, "bold")).pack(anchor="w")
            tk.Label(panel, text="Add a task and its subject will appear here.",
                     bg=WHITE, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 12))
            self._btn(panel, "+ Add task", self.add_task).pack(anchor="w")
            return
        for subject, count in sorted(counts.items()):
            panel = self._card(body, 18, 16)
            panel.pack(fill="x", pady=6)
            tk.Label(panel, text="▤   " + subject, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 11, "bold")).pack(side="left")
            tk.Label(panel, text=f"{count} task(s)", bg=PURPLE_SOFT, fg=PURPLE,
                     font=("Segoe UI", 9, "bold"), padx=10, pady=5).pack(side="right")

    def show_settings(self):
        self._clear()
        self._header("Settings", "Your StudyFlow workspace.",
                     "Application details and technology information.")
        panel = self._card(self.main, 24, 20)
        panel.pack(fill="x", padx=38)
        details = [
            ("Application", "StudyFlow — Student Planner"),
            ("Version", "3.0 — Refreshed desktop interface"),
            ("GUI framework", "Python Tkinter / ttk"),
            ("Database", "SQLite"),
            ("Password storage", "PBKDF2-HMAC-SHA256"),
        ]
        for label, value in details:
            line = tk.Frame(panel, bg=WHITE)
            line.pack(fill="x", pady=12)
            tk.Label(line, text=label, bg=WHITE, fg=MUTED,
                     font=("Segoe UI", 9)).pack(side="left")
            tk.Label(line, text=value, bg=WHITE, fg=TEXT,
                     font=("Segoe UI", 9, "bold")).pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyFlowApp(root)
    root.mainloop()
