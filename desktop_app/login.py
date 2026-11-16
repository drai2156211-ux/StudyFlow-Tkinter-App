import tkinter as tk
from tkinter import messagebox
from database import StudyFlowDatabase

BG = "#0B1020"
PANEL = "#111A2E"
CARD = "#17233B"
CARD_ALT = "#1D2B46"
PURPLE = "#8B5CF6"
WHITE = "#F8FAFC"
MUTED = "#9AAAC2"
BORDER = "#293854"

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.db = StudyFlowDatabase()
        self.root.title("StudyFlow | Welcome")
        self.root.geometry("1120x720")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children(): w.destroy()

    def _field(self, parent, label, show=None):
        tk.Label(parent, text=label.upper(), bg=CARD, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(13, 6))
        e = tk.Entry(parent, bg=CARD_ALT, fg=WHITE, insertbackground=WHITE,
                     relief="flat", bd=0, font=("Segoe UI", 11), show=show)
        e.pack(fill="x", ipady=12)
        return e

    def _layout(self, heading, subtitle, registration=False):
        self.clear()
        shell = tk.Frame(self.root, bg=BG); shell.pack(fill="both", expand=True, padx=45, pady=38)
        left = tk.Frame(shell, bg="#211A43", padx=35, pady=35,
                        highlightthickness=1, highlightbackground="#45366F")
        left.pack(side="left", fill="both", expand=True, padx=(0, 18))
        tk.Label(left, text="✦", bg="#211A43", fg="#C4B5FD", font=("Segoe UI", 32, "bold")).pack(anchor="w", pady=(20, 15))
        tk.Label(left, text="Study smarter.\nStay in control.", bg="#211A43", fg=WHITE,
                 font=("Segoe UI", 29, "bold"), justify="left").pack(anchor="w", pady=(5, 12))
        tk.Label(left, text="Your personal space to plan tasks, track deadlines\nand make steady progress throughout the semester.",
                 bg="#211A43", fg="#C4B5FD", font=("Segoe UI", 10), justify="left").pack(anchor="w")
        features = ["✓  Organise academic tasks", "✓  Track priorities and due dates", "✓  Review your study progress"]
        for f in features:
            tk.Label(left, text=f, bg="#211A43", fg="#E2DDF7", font=("Segoe UI", 10)).pack(anchor="w", pady=(24, 0))
        tk.Label(left, text="STUDYFLOW  •  STUDENT PRODUCTIVITY", bg="#211A43", fg="#8979B8",
                 font=("Segoe UI", 8, "bold")).pack(side="bottom", anchor="w")
        right = tk.Frame(shell, bg=CARD, padx=38, pady=32, width=390,
                         highlightthickness=1, highlightbackground=BORDER)
        right.pack(side="right", fill="y"); right.pack_propagate(False)
        tk.Label(right, text="StudyFlow", bg=CARD, fg=WHITE, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(28, 6))
        tk.Label(right, text=heading, bg=CARD, fg=WHITE, font=("Segoe UI", 17, "bold")).pack(anchor="w", pady=(20, 4))
        tk.Label(right, text=subtitle, bg=CARD, fg=MUTED, font=("Segoe UI", 9), wraplength=300, justify="left").pack(anchor="w", pady=(0, 12))
        return right

    def _action(self, parent, text, command):
        tk.Button(parent, text=text, command=command, bg=PURPLE, fg=WHITE,
                  activebackground="#7045D8", activeforeground=WHITE, bd=0,
                  font=("Segoe UI", 10, "bold"), cursor="hand2").pack(fill="x", ipady=12, pady=(24, 12))

    def show_login(self):
        card = self._layout("Welcome back", "Sign in to continue to your student workspace.")
        self.username = self._field(card, "Username")
        self.password = self._field(card, "Password", "•")
        self._action(card, "SIGN IN  →", self.login)
        tk.Button(card, text="Create a new account", command=self.show_register, bg=CARD, fg="#B9A4FF",
                  activebackground=CARD, activeforeground=WHITE, bd=0, font=("Segoe UI", 9, "bold"), cursor="hand2").pack(pady=8)
        self.username.focus_set()
        self.root.bind("<Return>", lambda _e: self.login())

    def show_register(self):
        card = self._layout("Create your account", "Set up your StudyFlow login. Your password is stored as a secure hash.", True)
        self.reg_username = self._field(card, "Choose username")
        self.reg_password = self._field(card, "Create password", "•")
        self.confirm_password = self._field(card, "Confirm password", "•")
        self._action(card, "CREATE ACCOUNT", self.register)
        tk.Button(card, text="← Back to sign in", command=self.show_login, bg=CARD, fg="#B9A4FF",
                  activebackground=CARD, activeforeground=WHITE, bd=0, font=("Segoe UI", 9, "bold"), cursor="hand2").pack(pady=5)

    def register(self):
        username = self.reg_username.get().strip()
        password = self.reg_password.get()
        confirm = self.confirm_password.get()
        if not username or not password or not confirm:
            messagebox.showwarning("Missing information", "Please fill in all fields.", parent=self.root); return
        if len(username) < 3:
            messagebox.showwarning("Username too short", "Use at least 3 characters.", parent=self.root); return
        if len(password) < 8:
            messagebox.showwarning("Password too short", "Use at least 8 characters.", parent=self.root); return
        if password != confirm:
            messagebox.showerror("Passwords do not match", "Please enter the same password twice.", parent=self.root); return
        if self.db.register_user(username, password):
            messagebox.showinfo("Account created", "Your account is ready. Please sign in.", parent=self.root)
            self.show_login()
            self.username.insert(0, username)
        else:
            messagebox.showerror("Username unavailable", "That username already exists. Try another.", parent=self.root)

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showwarning("Missing information", "Enter your username and password.", parent=self.root); return
        if not self.db.verify_user(username, password):
            messagebox.showerror("Sign-in failed", "The username or password is incorrect.", parent=self.root); return
        self.root.unbind("<Return>")
        for w in self.root.winfo_children(): w.destroy()
        self.root.geometry("1320x820"); self.root.minsize(1080, 700); self.root.resizable(True, True)
        from main import StudyFlowApp
        self.app = StudyFlowApp(self.root)

if __name__ == "__main__":
    root = tk.Tk(); app = LoginSystem(root); root.mainloop()
