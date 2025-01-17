import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from vfs_core import VFS


class VFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual File System (Cross-OS Support)")
        self.vfs = VFS()
        self.root.geometry("800x600")


        # Create menu bar
        menu_bar = Menu(self.root)

        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Create File", command=self.create_file)
        file_menu.add_command(label="Read File", command=self.read_file)
        file_menu.add_command(label="Update File", command=self.update_file)
        file_menu.add_command(label="Delete File", command=self.delete_file)
        file_menu.add_command(label="Search File", command=self.search_file)
        file_menu.add_separator()
        file_menu.add_command(label="Set Shared Directory", command=self.set_shared_directory)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Configure menu bar
        self.root.config(menu=menu_bar)

        # Instructions
        self.instructions = tk.Label(
            self.root,
            text="Welcome to the Virtual File System!\nUse the File menu to perform operations.\n\nFor more information, visit https://github.com/duttaturja/virtual-file-system\n\n\nCreated By:\n\n\tTurja Dutta\n\tShafin Shahriar\n\tYasir Zaman Alif\n\n\nSupervised By:\n\tProfessor Zainal Abedin",
            wraplength=400,
            justify="center",
        )
        self.instructions.pack(pady=20)

    def create_file(self):
        def save_file():
            file_name = file_name_entry.get()
            content = content_text.get("1.0", END).strip()
            if file_name:
                try:
                    self.vfs.create_file(file_name, content)
                    messagebox.showinfo("Success", f"File '{file_name}' created successfully.")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "File name cannot be empty.")

        # Create a dialog box
        dialog = Toplevel(self.root)
        dialog.title("Create File")
        dialog.geometry("400x300")

        Label(dialog, text="File Name:").pack(pady=5)
        file_name_entry = Entry(dialog, width=40)
        file_name_entry.pack(pady=5)

        Label(dialog, text="File Content:").pack(pady=5)
        content_text = ScrolledText(dialog, width=45, height=10)
        content_text.pack(pady=5)

        Button(dialog, text="Save", command=save_file).pack(pady=10, anchor="center")

    def read_file(self):
        def fetch_file():
            file_name = file_name_entry.get()
            if file_name:
                try:
                    content = self.vfs.read_file(file_name)
                    content_text.delete("1.0", END)
                    content_text.insert("1.0", content)
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        # Create a dialog box
        dialog = Toplevel(self.root)
        dialog.title("Read File")
        dialog.geometry("400x300")

        Label(dialog, text="File Name:").pack(pady=5)
        file_name_entry = Entry(dialog, width=40)
        file_name_entry.pack(pady=5)

        Button(dialog, text="Read", command=fetch_file).pack(pady=5)

        Label(dialog, text="File Content:").pack(pady=5)
        content_text = ScrolledText(dialog, width=45, height=10, state="normal")
        content_text.pack(pady=5)

    def update_file(self):
        def update_content():
            file_name = file_name_entry.get()
            content = content_text.get("1.0", END).strip()
            if file_name:
                try:
                    self.vfs.update_file(file_name, content)
                    messagebox.showinfo("Success", f"File '{file_name}' updated successfully.")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "File name cannot be empty.")

        # Create a dialog box
        dialog = Toplevel(self.root)
        dialog.title("Update File")
        dialog.geometry("400x300")

        Label(dialog, text="File Name:").pack(pady=5)
        file_name_entry = Entry(dialog, width=40)
        file_name_entry.pack(pady=5)

        Label(dialog, text="New Content:").pack(pady=5)
        content_text = ScrolledText(dialog, width=45, height=10)
        content_text.pack(pady=5)

        Button(dialog, text="Update", command=update_content).pack(pady=10)

    def delete_file(self):
        def confirm_delete():
            file_name = file_name_entry.get()
            if file_name:
                try:
                    self.vfs.delete_file(file_name)
                    messagebox.showinfo("Success", f"File '{file_name}' deleted successfully.")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            else:
                messagebox.showerror("Error", "File name cannot be empty.")

        # Create a dialog box
        dialog = Toplevel(self.root)
        dialog.title("Delete File")
        dialog.geometry("400x150")

        Label(dialog, text="File Name:").pack(pady=5)
        file_name_entry = Entry(dialog, width=40)
        file_name_entry.pack(pady=5)

        Button(dialog, text="Delete", command=confirm_delete).pack(pady=10)

    def search_file(self):
        def fetch_file():
            file_name = file_name_entry.get()
            if file_name:
                found, metadata = self.vfs.search_files(file_name)
                if found:
                    content = metadata["content"]
                    details = (
                        f"File Name: {file_name}\n"
                        f"Size: {metadata['size']} bytes\n"
                        f"Creation Time: {metadata['creation_time']}\n"
                        f"Content:\n{content}"
                    )
                    content_text.delete("1.0", END)
                    content_text.insert("1.0", details)
                else:
                    messagebox.showerror("Error", f"File '{file_name}' not found.")

        # Create a dialog box
        dialog = Toplevel(self.root)
        dialog.title("Search File")
        dialog.geometry("400x300")

        Label(dialog, text="File Name:").pack(pady=5)
        file_name_entry = Entry(dialog, width=40)
        file_name_entry.pack(pady=5)

        Button(dialog, text="Search", command=fetch_file).pack(pady=5)

        Label(dialog, text="File Details:").pack(pady=5)
        content_text = ScrolledText(dialog, width=45, height=10, state="normal")
        content_text.pack(pady=5)

    def set_shared_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            try:
                self.vfs.set_root_directory(directory)
                messagebox.showinfo("Success", f"Shared directory set to: {directory}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        else:
            messagebox.showerror("Error", "Shared directory cannot be empty.")

    


if __name__ == "__main__":
    root = Tk()
    app = VFSApp(root)
    root.mainloop()
