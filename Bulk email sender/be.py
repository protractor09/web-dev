import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import tempfile
import email_sender as es

class BulkEmailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulk Email Sender")
        self.root.configure(bg="white")

        self.attachments = []
        self.email_list = []

        self.create_intro_screen()

    def create_intro_screen(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        warning = (
            "📌 INSTRUCTIONS BEFORE USING THE APP:\n"
            "1. Upload a file in .csv, .xlsx, or .txt format.\n"
            "2. Must contain a column named: email, emails, Email, or Emails.\n"
            "3. Emails must be valid (e.g., someone@example.com).\n"
            "4. Empty cells are skipped automatically.\n"
            "5. Avoid duplicate email addresses.\n"
            "6. Do not exceed 500 emails/day using Gmail.\n"
            "7. Review email content and preview before sending.\n"
        )
        tk.Label(frame, text=warning, justify="left", fg="black", bg="white", font=("Arial", 10), anchor="w").pack(fill="x", pady=(0, 10))

        info = (
            "🔐 WHAT IS AN APP PASSWORD?\n"
            "Google no longer allows most apps to use your regular Gmail password.\n"
            "Instead, generate a special one-time password (App Password).\n\n"
            "✅ HOW TO GET ONE:\n"
            "1. Enable 2-Step Verification in your Gmail settings.\n"
            "2. Visit: https://myaccount.google.com/apppasswords\n"
            "3. Choose App: Mail | Device: Other (Windows Computer)\n"
            "4. Copy the 16-character password and paste it below.\n"
            "👉 Note: This is NOT your Gmail login password."
        )
        tk.Label(frame, text=info, justify="left", fg="blue", bg="white", font=("Arial", 10), anchor="w").pack(fill="x", pady=(0, 20))

        tk.Button(frame, text="✅ I Understand — Enter App", command=self.create_main_form).pack(pady=10)


    def create_main_form(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.email = tk.StringVar()
        self.password = tk.StringVar()
        self.subject = tk.StringVar()
        self.file_type = tk.StringVar(value='csv or excel')

        fields = [
            ("Your Email:", self.email),
            ("App Password:", self.password),
            ("Subject:", self.subject),
        ]

        for label_text, var in fields:
            tk.Label(frame, text=label_text, anchor="w", bg="white", fg="black").pack(fill="x")
            show_char = '*' if "Password" in label_text else None
            tk.Entry(frame, textvariable=var, show=show_char).pack(fill="x", pady=(0, 5))

        tk.Label(frame, text="Email Body (you can use {name} for name):", anchor="w", bg="white", fg="black").pack(fill="x")
        self.body_entry = tk.Text(frame, height=5)
        self.body_entry.pack(fill="x", pady=(0,10))

        tk.Button(frame, text="Attach Files", command=self.select_attachments).pack(pady=5)

        ttk.Combobox(frame, values=["csv or excel", "text"], textvariable=self.file_type).pack(fill="x")

        tk.Button(frame, text="Upload Recipient File", command=self.upload_file).pack(pady=5)

        self.send_button = tk.Button(frame, text="Send Emails", command=self.send_emails)
        self.send_button.pack(pady=10)

        tk.Label(frame, text="📎 Attached Files:", anchor="w", bg="white", fg="black").pack(fill="x", pady=(10, 0))
        self.attachment_listbox = tk.Listbox(frame, height=5)
        self.attachment_listbox.pack(fill="x", pady=(0, 10))

        tk.Label(frame, text="📬 Recipient Emails:", anchor="w", bg="white", fg="black").pack(fill="x", pady=(10, 0))
        self.email_listbox = tk.Listbox(frame, height=5)
        self.email_listbox.pack(fill="x", pady=(0, 10))

        self.log_text = tk.Text(frame, height=10)
        self.log_text.pack(fill="x", pady=(10,0))

    def select_attachments(self):
        files = filedialog.askopenfilenames()
        self.attachments = []
        self.attachment_listbox.delete(0, tk.END)

        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.basename(file)) as tmp:
                tmp.write(open(file, 'rb').read())
                self.attachments.append(tmp.name)
                self.attachment_listbox.insert(tk.END, os.path.basename(file))

        self.log(f"Attached {len(self.attachments)} file(s).")

    def upload_file(self):
        self.email_listbox.delete(0, tk.END)
        ftype = self.file_type.get()
        if ftype == 'csv or excel':
            file = filedialog.askopenfilename(filetypes=[("CSV or Excel", "*.csv *.xlsx")])
            if file:
                try:
                    df = pd.read_csv(file) if file.endswith(".csv") else pd.read_excel(file)
                    self.email_list = []
                    for col in ['email', 'emails', 'Email', 'Emails']:
                        if col in df.columns:
                            self.email_list = [str(e).strip() for e in df[col].dropna() if es.is_valid_email(str(e))]
                            break
                    for email in self.email_list:
                        self.email_listbox.insert(tk.END, email)
                    self.log(f"Loaded {len(self.email_list)} valid email(s).")
                except Exception as e:
                    self.log(f"Error reading file: {e}")
        else:
            file = filedialog.askopenfilename(filetypes=[("Text File", "*.txt")])
            if file:
                with open(file, 'rb') as f:
                    self.email_list = es.get_email_txt(f)
                for email in self.email_list:
                    self.email_listbox.insert(tk.END, email)
                self.log(f"Loaded {len(self.email_list)} valid email(s).")

    def send_emails(self):
        email = self.email.get()
        password = self.password.get()
        subject = self.subject.get()
        body = self.body_entry.get("1.0", tk.END).strip()

        if not (email and password and subject and body):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.email_list:
            messagebox.showerror("Error", "No valid emails to send.")
            return

        self.log("Sending emails...")
        try:
            es.logic(email, password, body, subject, self.email_list, self.attachments)
            self.log("✅ All emails processed.")
        except Exception as e:
            self.log(f"❌ Error sending emails: {e}")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BulkEmailApp(root)
    root.mainloop()
