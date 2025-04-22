import tkinter as tk
from tkinter import messagebox, simpledialog
import csv, os
from datetime import datetime

data_file = 'tasks.csv'
history_file = 'history.csv'
fieldnames = ['Timestamp', 'Task']
fieldnames2 = ['Timestamp', 'Task', 'DeletedOn']

def current_time():
    return datetime.now().strftime("%d-%m-%Y @ %H:%M")

class RoyalToDo:
    def __init__(self, root):
        self.root = root
        self.root.title("🖤 Golden Task Tracker")
        self.root.geometry("520x620")
        self.root.config(bg="#000000")

        self.tasks = []
        self.deleted_tasks = []
        self.load_data()

        tk.Label(root, text="To-Do List", font=("Georgia", 22, "bold"), 
                 bg="#000000", fg="#FFD700").pack(pady=20)

        self.listbox = tk.Listbox(root, font=("Georgia", 12), height=14, width=50,
                                  bg="#111111", fg="#FFD700", selectbackground="#FFD700",
                                  selectforeground="#000", relief="flat", highlightthickness=0)
        self.listbox.pack(pady=10)

        self.create_buttons()

        tk.Label(root, text="Built with class and code ✨", font=("Georgia", 10),
                 bg="#000000", fg="#888").pack(pady=10)

        self.display_tasks()

        # Adding the protocol to handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_buttons(self):
        btn_frame = tk.Frame(self.root, bg="#000000")
        btn_frame.pack(pady=10)

        style = {
            "font": ("Georgia", 11),
            "bg": "#222222", "fg": "#FFD700",
            "activebackground": "#FFD700",
            "activeforeground": "#000",
            "width": 20, "height": 2,
            "relief": "flat", "bd": 0,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="➕ Add Task", command=self.add_task, **style).grid(row=0, column=0, padx=10, pady=6)
        tk.Button(btn_frame, text="❌ Remove Task", command=self.delete_task, **style).grid(row=1, column=0, padx=10, pady=6)
        tk.Button(btn_frame, text="📜 History", command=self.show_history, **style).grid(row=2, column=0, padx=10, pady=6)
        tk.Button(btn_frame, text="💾 Save & Exit", command=self.save_and_exit, **style).grid(row=3, column=0, padx=10, pady=6)

    def load_data(self):
        if os.path.exists(data_file):
            with open(data_file, newline='') as f:
                self.tasks = list(csv.DictReader(f))

        if os.path.exists(history_file):
            with open(history_file, newline='') as f:
                self.deleted_tasks = list(csv.DictReader(f))

    def display_tasks(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, f"• {task['Task']} | ⏱ {task['Timestamp']}")

    def add_task(self):
        task = simpledialog.askstring("Add New Task", "Enter a task:", parent=self.root)
        if task:
            self.tasks.append({'Timestamp': current_time(), 'Task': task})
            self.display_tasks()

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Oops!", "Select a task to delete.")
            return
        index = selected[0]
        deleted = self.tasks.pop(index)
        deleted['DeletedOn'] = current_time()
        self.deleted_tasks.append(deleted)
        self.display_tasks()
        messagebox.showinfo("Deleted", "Task removed.")

    def show_history(self):
        if not self.deleted_tasks:
            messagebox.showinfo("No History", "No deleted tasks yet.")
            return
        msg = "\n\n".join([f"{t['Task']} \n⏱ Added: {t['Timestamp']} → ❌ Deleted: {t['DeletedOn']}"
                          for t in self.deleted_tasks])
        messagebox.showinfo("Deleted Tasks", msg)

    def save_and_exit(self):
        self.save_data()
        messagebox.showinfo("Saved", "All tasks saved. Bye boss!")
        self.root.destroy()

    def save_data(self):
        with open(data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.tasks)

        with open(history_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames2)
            writer.writeheader()
            writer.writerows(self.deleted_tasks)

    def on_closing(self):
        answer = messagebox.askyesnocancel("Quit", "Do you want to save your tasks before exiting?")
        if answer is None:  # Cancel button was clicked
            return
        elif answer:  # Yes was clicked
            self.save_data()
            messagebox.showinfo("Saved", "Tasks saved successfully!")
            self.root.destroy()
        else:  # No was clicked
            self.root.destroy()

# ==== RUN ==== 
if __name__ == "__main__":
    root = tk.Tk()
    app = RoyalToDo(root)
    root.mainloop()
