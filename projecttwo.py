#Project Two: Code Focus

#imports
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Listbox, Toplevel, END, Scrollbar
from cryptography.fernet import Fernet
import json
import os
import random
import string
import csv

# Define file paths for the secret key and the encrypted passwords file
KEY_FILE = 'secret.key'
PASSWORDS_FILE = 'passwords.json'

# Generate a new encryption key
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)
    return key

# Load the encryption key from file
def load_key():
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

# Encrypt the data using the loaded key
def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

# Decrypt the data using the loaded key
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data).decode()

# Load passwords from the encrypted file
def load_passwords():
    if os.path.exists(PASSWORDS_FILE):
        with open(PASSWORDS_FILE, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = decrypt_data(encrypted_data, key)
        return json.loads(decrypted_data)
    return []

# Save passwords to the encrypted file
def save_passwords(passwords):
    data_to_encrypt = json.dumps(passwords, indent=4)
    encrypted_data = encrypt_data(data_to_encrypt, key)
    with open(PASSWORDS_FILE, 'wb') as file:
        file.write(encrypted_data)

# Generate a random password
def generate_password(length=12, include_special_chars=True):
    if length < 8:
        length = 8
    characters = string.ascii_letters + string.digits
    if include_special_chars:
        characters += string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Load or generate the encryption key
key = load_key() if os.path.exists(KEY_FILE) else generate_key()
# Load existing passwords
passwords = load_passwords()

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Password Manager')
        self.geometry('600x400')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.configure_gui_styles()
        self.init_ui()

    # Configure styles for the GUI elements
    def configure_gui_styles(self):
        self.style.configure('TButton', font=('Helvetica', 12), foreground='blue', background='light gray')
        self.style.map('TButton', foreground=[('active', 'green')], background=[('active', 'light blue')])
        self.style.configure('TLabel', font=('Helvetica', 12), foreground='dark green')
        self.style.configure('TFrame', background='light blue')

    # Initialize the UI - setup layout and buttons
    def init_ui(self):
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Button to add a new password
        self.add_button = ttk.Button(frame, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=5, fill=tk.X)

        # Button to view saved passwords
        self.view_button = ttk.Button(frame, text="View Passwords", command=self.view_passwords)
        self.view_button.pack(pady=5, fill=tk.X)

        # Button to delete a specific password
        self.delete_button = ttk.Button(frame, text="Delete Password", command=self.delete_password)
        self.delete_button.pack(pady=5, fill=tk.X)

        # Button to export passwords to a CSV file
        self.export_button = ttk.Button(frame, text="Export Passwords to CSV", command=self.export_passwords_to_csv)
        self.export_button.pack(pady=5, fill=tk.X)

        # Button to import passwords from a CSV file
        self.import_button = ttk.Button(frame, text="Import Passwords from CSV", command=self.import_passwords_from_csv)
        self.import_button.pack(pady=5, fill=tk.X)

        # Button to exit the application
        self.exit_button = ttk.Button(frame, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=5, fill=tk.X)

        # Button to delete all passwords and exit the application
        self.delete_all_exit_button = ttk.Button(frame, text="Delete All & Exit", command=self.delete_all_and_exit)
        self.delete_all_exit_button.pack(pady=5, fill=tk.X)

    # Add a new password entry
    def add_password(self):
        service = simpledialog.askstring("Add Password", "Enter the service name:", parent=self)
        if service:
            use_generated_password = messagebox.askyesno("Password", "Do you want to generate a password?", parent=self)
            if use_generated_password:
                length = simpledialog.askinteger("Password Length", "Enter the desired password length:",
                                                 initialvalue=12, minvalue=8, maxvalue=128, parent=self)
                include_special_chars = messagebox.askyesno("Include Special Characters",
                                                            "Do you want to include special characters in your password?",
                                                            parent=self)
                password = generate_password(length, include_special_chars)
            else:
                password = simpledialog.askstring("Add Password", "Enter the password:", parent=self, show='*')
                if not password:
                    return
            passwords.append({'service': service, 'password': password})
            save_passwords(passwords)
            messagebox.showinfo("Success", "Password added successfully", parent=self)

    # View saved passwords
    def view_passwords(self):
        passwords_window = Toplevel(self)
        passwords_window.title("View Passwords")
        passwords_window.geometry('400x300')
        scrollbar = Scrollbar(passwords_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox = Listbox(passwords_window, yscrollcommand=scrollbar.set)
        for item in passwords:
            listbox.insert(END, f"{item['service']}: {item['password']}")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

    # Delete a specific password
    def delete_password(self):
        def confirm_delete():
            selection = listbox.curselection()
            if selection:
                selected_index = selection[0]
                if messagebox.askyesno("Confirm", "Are you sure you want to delete this password?",
                                       parent=delete_window):
                    del passwords[selected_index]
                    save_passwords(passwords)
                    listbox.delete(selected_index)

        delete_window = Toplevel(self)
        delete_window.title("Delete Password")
        listbox = Listbox(delete_window, width=50, height=15)
        for item in passwords:
            listbox.insert(END, f"{item['service']}: {item['password']}")
        listbox.pack(padx=10, pady=10)
        delete_btn = ttk.Button(delete_window, text="Delete Selected", command=confirm_delete)
        delete_btn.pack(pady=5)

    # Delete all passwords and exit the application
    def delete_all_and_exit(self):
        if messagebox.askyesno("Confirm Delete All",
                               "This will delete all stored passwords and exit the program. Are you sure?",
                               parent=self):
            try:
                os.remove(PASSWORDS_FILE)
                os.remove(KEY_FILE)
                messagebox.showinfo("Deleted", "All data deleted successfully.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete data: {str(e)}", parent=self)
            self.destroy()

    # Export saved passwords to a CSV file
    def export_passwords_to_csv(self):
        export_file = 'passwords_export.csv'
        with open(export_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Service', 'Password'])
            for item in passwords:
                writer.writerow([item['service'], item['password']])
        messagebox.showinfo("Export Successful", f"Passwords exported to {export_file}")

    # Import passwords from a CSV file
    def import_passwords_from_csv(self):
        import_file = simpledialog.askstring("Import Passwords", "Enter the CSV file name:", parent=self)
        if import_file:
            try:
                with open(import_file, mode='r', newline='') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        passwords.append({'service': row['Service'], 'password': row['Password']})
                save_passwords(passwords)
                messagebox.showinfo("Import Successful", "Passwords imported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import passwords: {str(e)}", parent=self)

# Run the thing!
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
